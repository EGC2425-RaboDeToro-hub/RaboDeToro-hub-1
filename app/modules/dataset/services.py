import logging
import os
import hashlib
import shutil
from typing import Optional
import uuid
import tempfile

from flask import request
from zipfile import ZipFile

from app.modules.auth.services import AuthenticationService
from app.modules.dataset.models import DSViewRecord, DataSet, DSMetaData
from app.modules.dataset.repositories import (
    AuthorRepository,
    DOIMappingRepository,
    DSDownloadRecordRepository,
    DSMetaDataRepository,
    DSViewRecordRepository,
    DataSetRepository,
)
from app.modules.featuremodel.repositories import (
    FMMetaDataRepository,
    FeatureModelRepository,
)
from app.modules.hubfile.repositories import (
    HubfileDownloadRecordRepository,
    HubfileRepository,
    HubfileViewRecordRepository,
)
from core.services.BaseService import BaseService
from flamapy.metamodels.fm_metamodel.transformations import (
    UVLReader,
    GlencoeWriter,
    SPLOTWriter,
)
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat, DimacsWriter

logger = logging.getLogger(__name__)


def calculate_checksum_and_size(file_path):
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as file:
        content = file.read()
        hash_md5 = hashlib.md5(content).hexdigest()
        return hash_md5, file_size


class DataSetService(BaseService):
    def __init__(self):
        super().__init__(DataSetRepository())
        self.feature_model_repository = FeatureModelRepository()
        self.author_repository = AuthorRepository()
        self.dsmetadata_repository = DSMetaDataRepository()
        self.fmmetadata_repository = FMMetaDataRepository()
        self.dsdownloadrecord_repository = DSDownloadRecordRepository()
        self.hubfiledownloadrecord_repository = HubfileDownloadRecordRepository()
        self.hubfilerepository = HubfileRepository()
        self.dsviewrecord_repostory = DSViewRecordRepository()
        self.hubfileviewrecord_repository = HubfileViewRecordRepository()
        self.repository = DataSetRepository()

    def move_feature_models(self, dataset: DataSet):
        current_user = AuthenticationService().get_authenticated_user()
        source_dir = current_user.temp_folder()

        working_dir = os.getenv("WORKING_DIR", "")
        dest_dir = os.path.join(
            working_dir, "uploads", f"user_{current_user.id}", f"dataset_{dataset.id}"
        )

        os.makedirs(dest_dir, exist_ok=True)

        for feature_model in dataset.feature_models:
            uvl_filename = feature_model.fm_meta_data.uvl_filename
            shutil.move(os.path.join(source_dir, uvl_filename), dest_dir)

    def is_synchronized(self, dataset_id: int) -> bool:
        return self.repository.is_synchronized(dataset_id)

    def get_synchronized(self, current_user_id: int) -> DataSet:
        return self.repository.get_synchronized(current_user_id)

    def get_unsynchronized(self, current_user_id: int) -> DataSet:
        return self.repository.get_unsynchronized(current_user_id)

    def get_unsynchronized_dataset(
        self, current_user_id: int, dataset_id: int
    ) -> DataSet:
        return self.repository.get_unsynchronized_dataset(current_user_id, dataset_id)

    def latest_synchronized(self):
        return self.repository.latest_synchronized()

    def count_synchronized_datasets(self):
        return self.repository.count_synchronized_datasets()

    def count_feature_models(self):
        return self.feature_model_service.count_feature_models()

    def count_authors(self) -> int:
        return self.author_repository.count()

    def count_dsmetadata(self) -> int:
        return self.dsmetadata_repository.count()

    def total_dataset_downloads(self) -> int:
        return self.dsdownloadrecord_repository.total_dataset_downloads()

    def total_dataset_views(self) -> int:
        return self.dsviewrecord_repostory.total_dataset_views()

    def create_from_form(self, form, current_user) -> DataSet:
        # Definir el autor principal
        main_author = {
            "name": f"{current_user.profile.surname}, {current_user.profile.name}",
            "affiliation": current_user.profile.affiliation,
            "orcid": current_user.profile.orcid,
        }
        try:
            logger.info(f"Creating dsmetadata...: {form.get_dsmetadata()}")

            # Crear DSMetaData
            dsmetadata = self.dsmetadata_repository.create(**form.get_dsmetadata())

            # Agregar autores principales y adicionales
            for author_data in [main_author] + form.get_authors():
                author = self.author_repository.create(
                    commit=False, ds_meta_data_id=dsmetadata.id, **author_data
                )
                dsmetadata.authors.append(author)

            # Crear el dataset
            dataset = self.create(
                commit=False, user_id=current_user.id, ds_meta_data_id=dsmetadata.id
            )

            # Procesar cada modelo UVL del formulario
            for feature_model in form.feature_models:
                uvl_filename = feature_model.uvl_filename.data

                # Crear FMMetaData
                fmmetadata = self.fmmetadata_repository.create(
                    commit=False, **feature_model.get_fmmetadata()
                )

                # Agregar autores al modelo UVL
                for author_data in feature_model.get_authors():
                    author = self.author_repository.create(
                        commit=False, fm_meta_data_id=fmmetadata.id, **author_data
                    )
                    fmmetadata.authors.append(author)

                # Crear el modelo de características
                fm = self.feature_model_repository.create(
                    commit=False, data_set_id=dataset.id, fm_meta_data_id=fmmetadata.id
                )

                # Procesar el archivo UVL
                file_path = os.path.join(current_user.temp_folder(), uvl_filename)
                checksum, size = calculate_checksum_and_size(file_path)

                # Crear el archivo relacionado con el modelo
                file = self.hubfilerepository.create(
                    commit=False,
                    name=uvl_filename,
                    checksum=checksum,
                    size=size,
                    feature_model_id=fm.id,
                )
                fm.files.append(file)

            # Guardar los cambios en la base de datos
            self.repository.session.commit()
        except Exception as exc:
            logger.info(f"Exception creating dataset from form...: {exc}")
            self.repository.session.rollback()
            raise exc

        return dataset

    def update_dsmetadata(self, id, **kwargs):
        return self.dsmetadata_repository.update(id, **kwargs)

    def get_uvlhub_doi(self, dataset: DataSet) -> str:
        domain = os.getenv("DOMAIN", "localhost")
        return f"http://{domain}/doi/{dataset.ds_meta_data.dataset_doi}"

    def zip_dataset(self, dataset: DataSet) -> str:
        working_dir = os.getenv("WORKING_DIR", "")
        file_path = os.path.join(
            working_dir, "uploads", f"user_{dataset.user_id}", f"dataset_{dataset.id}"
        )
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"dataset_{dataset.id}.zip")

        with ZipFile(zip_path, "w") as zipf:
            for subdir, dirs, files in os.walk(file_path):
                for file in files:
                    full_path = os.path.join(subdir, file)

                    relative_path = os.path.relpath(full_path, file_path)

                    zipf.write(
                        full_path,
                        arcname=os.path.join(
                            os.path.basename(zip_path[:-4]), relative_path
                        ),
                    )

        return temp_dir

    def zip_all_datasets(self) -> str:
        """
        Genera un archivo ZIP con todos los datasets sincronizados, incluyendo los formatos exportados.
        """
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "all_datasets.zip")
        try:
            with ZipFile(zip_path, "w") as zipf:
                logger.info(
                    "Iniciando la creación del archivo ZIP de todos los datasets sincronizados."
                )

                for user_dir in os.listdir("uploads"):
                    user_path = os.path.join("uploads", user_dir)
                    if os.path.isdir(user_path) and user_dir.startswith("user_"):
                        for dataset_dir in os.listdir(user_path):
                            dataset_path = os.path.join(user_path, dataset_dir)
                            if os.path.isdir(dataset_path) and dataset_dir.startswith(
                                "dataset_"
                            ):
                                dataset_id = int(dataset_dir.split("_")[1])
                                if self.is_synchronized(dataset_id):
                                    for subdir, _, files in os.walk(dataset_path):
                                        for file in files:
                                            if file.endswith(".uvl"):
                                                full_path = os.path.join(subdir, file)

                                                # Añadir archivo UVL original
                                                zipf.write(
                                                    full_path,
                                                    arcname=f"{user_dir}/{dataset_dir}/{file}",
                                                )

                                                # Generar y añadir exportaciones
                                                for format in [
                                                    "glencoe",
                                                    "dimacs",
                                                    "splot",
                                                ]:
                                                    try:
                                                        converted_content = (
                                                            self.convert_to_format(
                                                                full_path, format
                                                            )
                                                        )
                                                        if converted_content:
                                                            converted_file_name = (
                                                                file.replace(
                                                                    ".uvl",
                                                                    f".{format}.txt",
                                                                )
                                                            )
                                                            arcname = f"{user_dir}/{dataset_dir}/{converted_file_name}"
                                                            zipf.writestr(
                                                                arcname,
                                                                converted_content,
                                                            )
                                                    except Exception as e:
                                                        logger.error(
                                                            f"Error al convertir {file} a {format}: {e}"
                                                        )
        except Exception as e:
            logger.error(f"Error al crear el archivo ZIP: {e}")
            raise e
        return zip_path

    def convert_to_format(self, file_path: str, format: str) -> Optional[str]:
        try:
            # Diccionario con las clases de conversión
            writer_classes = {
                "glencoe": GlencoeWriter,
                "dimacs": DimacsWriter,
                "splot": SPLOTWriter,
            }

            if format == "uvl":
                with open(file_path, "r") as uvl_file:
                    return uvl_file.read()

            if format not in writer_classes:
                logger.error(f"Formato desconocido: {format}")
                return None

            temp_file = tempfile.NamedTemporaryFile(delete=False)
            try:
                fm = UVLReader(file_path).transform()
                if format == "dimacs":
                    sat = FmToPysat(fm).transform()
                    writer_classes[format](temp_file.name, sat).transform()
                else:
                    writer_classes[format](temp_file.name, fm).transform()

                # Leer y devolver el contenido convertido
                with open(temp_file.name, "r") as converted_file:
                    return converted_file.read()
            finally:
                # Limpiar el archivo temporal
                os.remove(temp_file.name)

        except Exception as e:
            logger.error(f"Error al convertir el archivo {file_path} a {format}: {e}")
            return None


class AuthorService(BaseService):
    def __init__(self):
        super().__init__(AuthorRepository())


class DSDownloadRecordService(BaseService):
    def __init__(self):
        super().__init__(DSDownloadRecordRepository())


class DSMetaDataService(BaseService):
    def __init__(self):
        super().__init__(DSMetaDataRepository())

    def update(self, id, **kwargs):
        return self.repository.update(id, **kwargs)

    def filter_by_doi(self, doi: str) -> Optional[DSMetaData]:
        return self.repository.filter_by_doi(doi)


class DSViewRecordService(BaseService):
    def __init__(self):
        super().__init__(DSViewRecordRepository())

    def the_record_exists(self, dataset: DataSet, user_cookie: str):
        return self.repository.the_record_exists(dataset, user_cookie)

    def create_new_record(self, dataset: DataSet, user_cookie: str) -> DSViewRecord:
        return self.repository.create_new_record(dataset, user_cookie)

    def create_cookie(self, dataset: DataSet) -> str:

        user_cookie = request.cookies.get("view_cookie")
        if not user_cookie:
            user_cookie = str(uuid.uuid4())

        existing_record = self.the_record_exists(
            dataset=dataset, user_cookie=user_cookie
        )

        if not existing_record:
            self.create_new_record(dataset=dataset, user_cookie=user_cookie)

        return user_cookie


class DOIMappingService(BaseService):
    def __init__(self):
        super().__init__(DOIMappingRepository())

    def get_new_doi(self, old_doi: str) -> str:
        doi_mapping = self.repository.get_new_doi(old_doi)
        if doi_mapping:
            return doi_mapping.dataset_doi_new
        else:
            return None


class SizeService:

    def __init__(self):
        pass

    def get_human_readable_size(self, size: int) -> str:
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024**2:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024**3:
            return f"{round(size / (1024 ** 2), 2)} MB"
        else:
            return f"{round(size / (1024 ** 3), 2)} GB"
