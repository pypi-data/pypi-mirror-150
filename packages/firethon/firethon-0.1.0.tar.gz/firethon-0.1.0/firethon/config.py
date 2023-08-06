from dataclasses import dataclass


@dataclass
class FirebaseConfig:
    url: str
    path_to_service_account_file: str
