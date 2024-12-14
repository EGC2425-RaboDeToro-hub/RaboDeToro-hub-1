import os
import shutil
import re
from app.modules.auth.models import User
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    Author
)
from datetime import datetime, timezone
from dotenv import load_dotenv
from app import db


class DataSetSeeder(BaseSeeder):
    priority = 2  # Lower priority

    def count_features_in_uvl(self, file_path):
        """Cuenta características dentro de la sección 'features' de un archivo UVL."""
        with open(file_path, 'r') as file:
            content = file.read()

            # Extraer la sección 'features'
            features_section = re.search(r'features\s+(.+?)constraints', content, re.DOTALL)
            if not features_section:
                return 0  # Si no hay sección de características, devolver 0

            # Contar líneas válidas dentro de 'features'
            features_content = features_section.group(1)
            return len(re.findall(r'^[ \t]*[^\s#]+[ \t]*$', features_content, re.MULTILINE))

    def run(self):
        # Limpieza de tablas relacionadas para evitar duplicados
        db.session.query(Hubfile).delete()
        db.session.query(FeatureModel).delete()
        db.session.query(FMMetaData).delete()
        db.session.query(DataSet).delete()
        db.session.query(DSMetaData).delete()
        db.session.query(DSMetrics).delete()
        db.session.query(Author).delete()
        db.session.commit()

        # Retrieve users
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        # Crear DSMetaData instances
        ds_meta_data_list = [
            DSMetaData(
                deposition_id=1 + i,
                title=f'Sample dataset {i+1}',
                description=f'Description for dataset {i+1}',
                publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
                publication_doi=f'10.1234/dataset{i+1}',
                dataset_doi=f'10.1234/dataset{i+1}',
                tags='tag1, tag2'
            ) for i in range(4)
        ]
        seeded_ds_meta_data = self.seed(ds_meta_data_list)

        # Crear Author instances y asociarlos con DSMetaData
        authors = [
            Author(
                name=f'Author {i+1}',
                affiliation=f'Affiliation {i+1}',
                orcid=f'0000-0000-0000-000{i}',
                ds_meta_data_id=seeded_ds_meta_data[i % 4].id
            ) for i in range(4)
        ]
        self.seed(authors)

        # Crear DataSet instances
        datasets = [
            DataSet(
                user_id=user1.id if i % 2 == 0 else user2.id,
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=datetime.now(timezone.utc)
            ) for i in range(4)
        ]
        seeded_datasets = self.seed(datasets)

        # Crear FMMetaData y FeatureModel instances
        fm_meta_data_list = [
            FMMetaData(
                uvl_filename=f'file{i+1}.uvl',
                title=f'Feature Model {i+1}',
                description=f'Description for feature model {i+1}',
                publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
                publication_doi=f'10.1234/fm{i+1}',
                tags='tag1, tag2',
                uvl_version='1.0'
            ) for i in range(12)
        ]
        seeded_fm_meta_data = self.seed(fm_meta_data_list)

        feature_models = [
            FeatureModel(
                data_set_id=seeded_datasets[i // 3].id,
                fm_meta_data_id=seeded_fm_meta_data[i].id
            ) for i in range(12)
        ]
        seeded_feature_models = self.seed(feature_models)

        # Procesar archivos UVL y calcular métricas
        load_dotenv()
        working_dir = os.getenv('WORKING_DIR', '')
        src_folder = os.path.join(working_dir, 'app', 'modules', 'dataset', 'uvl_examples')

        for dataset in seeded_datasets:
            total_features = 0
            total_models = 0

            # Iterar sobre los modelos de características del dataset
            for feature_model in [fm for fm in seeded_feature_models if fm.data_set_id == dataset.id]:
                file_name = feature_model.fm_meta_data.uvl_filename
                file_path = os.path.join(src_folder, file_name)

                if os.path.exists(file_path):
                    # Contar las características del archivo UVL
                    feature_count = self.count_features_in_uvl(file_path)
                    total_features += feature_count

                total_models += 1

            # Crear las métricas DSMetrics y asociarlas al dataset
            ds_metrics = DSMetrics(
                number_of_models=str(total_models),  # Convertir a string para el modelo
                number_of_features=str(total_features)  # Convertir a string
            )
            seeded_ds_metrics = self.seed([ds_metrics])[0]
            dataset.ds_meta_data.ds_metrics_id = seeded_ds_metrics.id

        # Crear archivos UVL y asociarlos con FeatureModels
        for i in range(12):
            file_name = f'file{i+1}.uvl'
            feature_model = seeded_feature_models[i]
            dataset = next(ds for ds in seeded_datasets if ds.id == feature_model.data_set_id)
            user_id = dataset.user_id

            dest_folder = os.path.join(working_dir, 'uploads', f'user_{user_id}', f'dataset_{dataset.id}')
            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy(os.path.join(src_folder, file_name), dest_folder)

            file_path = os.path.join(dest_folder, file_name)

            uvl_file = Hubfile(
                name=file_name,
                checksum=f'checksum{i+1}',
                size=os.path.getsize(file_path),
                feature_model_id=feature_model.id
            )
            self.seed([uvl_file])
