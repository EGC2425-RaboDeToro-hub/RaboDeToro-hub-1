from app.modules.fakenodo.repositories import FakenodoRepository
from core.services.BaseService import BaseService
from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
import logging
import os

from flask_login import current_user

logger = logging.getLogger(__name__)


class FakenodoService(BaseService):

    def __init__(self):
        self.deposition_repository = FakenodoRepository()

    def _generate_doi(self, dep_id):
        """Generate a fake DOI based on the deposition ID."""
        return f"10.1234/dataset{dep_id}"

    def test_connection(self):
        return True

    def create_new_deposition(self, dataset: DataSet):
        dep_id = dataset.id
        doi = self._generate_doi(dep_id)

        dpe_md = {
            "title": dataset.ds_meta_data.title,
            "upload_type": "dataset" if dataset.ds_meta_data.publication_type.value == "none" else "publication",
            "publication_type": (
                dataset.ds_meta_data.publication_type.value
                if dataset.ds_meta_data.publication_type.value != "none"
                else None
            ),
            "description": dataset.ds_meta_data.description,
            "creators": [
                {
                    "name": author.name,
                    **({"affiliation": author.affiliation} if author.affiliation else {}),
                    **({"orcid": author.orcid} if author.orcid else {}),
                }
                for author in dataset.ds_meta_data.authors
            ],
            "keywords": (
                ["uvlhub"] if not dataset.ds_meta_data.tags else dataset.ds_meta_data.tags.split(", ") + ["uvlhub"]
            ),
            "access_right": "open",
            "license": "CC-BY-4.0"
        }

        deposition = self.deposition_repository.create_new_deposition(doi, dpe_md)

        return {
            "dep_id": deposition.id,
            "doi": doi,
            "dpe_md": dpe_md,
            "message": "Deposition successfully created in Fakenodo"
        }

    def upload_file(self, dataset: DataSet, dep_id: str, feature_model: FeatureModel, user=None):
        if dep_id not in self.depositions:
            raise Exception("Deposition not found.")

        file_name = feature_model.fm_meta_data.uvl_filename
        file_path = os.path.join("uploads", f"user_{str(current_user.id)}", f"dataset_{dataset.id}", file_name)

        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("Simulated file content.")

        self.depositions[dep_id]["files"].append(file_name)

        file_metadata = {
            "file_name": file_name,
            "file_size": os.path.getsize(file_path),
            "file_url": f"/uploads/user_{current_user.id}/dataset_{dataset.id}/{file_name}",
            "upload_time": "2024-12-01T12:00:00",
        }

        return {
            "message": f"File {file_name} uploaded successfully.",
            "file_metadata": file_metadata
        }

    def publish_deposition(self, dep_id: str) -> dict:
        deposition = self.depositions.get(dep_id)

        if not deposition:
            raise Exception(f"Deposition with ID {dep_id} not found.")

        try:
            deposition["doi"] = f"fakenodo.doi.{dep_id}"
            deposition["status"] = "published"

            self.depositions[dep_id] = deposition

            response = {
                "id": dep_id,
                "status": "published",
                "conceptdoi": deposition["doi"],
                "message": "Deposition published successfully in Fakenodo."
            }
            return response

        except Exception as error:
            raise Exception(f"Failed to publish deposition with error: {str(error)}")

    def get_deposition(self, dep_id: str):
        deposition = self.deposition_repository.get_by_id(dep_id)
        if not deposition:
            raise Exception("Deposition not found.")
        return deposition

    def get_doi(self, dep_id: str) -> str:
        """
        Simulate getting a DOI for a deposition.

        If the DOI is not already generated, we will create one and store it in the deposition metadata.
        """
        if dep_id not in self.depositions:
            raise Exception(f"Deposition with ID {dep_id} not found.")

        # Check if DOI is already assigned, otherwise generate one
        deposition_metadata = self.depositions[dep_id]["metadata"]
        if "doi" not in deposition_metadata:
            # Simulate DOI generation (format: 10.xxxx/yyyyyy)
            # You could use UUID or the dataset ID to make the DOI unique
            generated_doi = self._generate_doi(dep_id)
            deposition_metadata["doi"] = generated_doi
        return deposition_metadata["doi"]

    def get_all_depositions(self):
        depositions = self.deposition_repository.get_all()
        return depositions

    def delete_deposition(self, dep_id: str) -> dict:
        """
        Simulate deleting a deposition from Fakenodo.
        """
        if dep_id not in self.depositions:
            raise Exception("Deposition not found.")

        # Simulate deletion
        self.deposition_repository.delete(dep_id)

        return {"message": "Deposition deleted successfully."}
