from huggingface_hub import HfApi
import os

REPO_ID = "vonWerlich/NEXT_Xadrez_Lichess_tournaments"

def main():
    api = HfApi()

    api.upload_folder(
        repo_id=REPO_ID,
        repo_type="dataset",
        folder_path="hf_dataset",
        path_in_repo="",
        commit_message="Atualização automática via GitHub Actions"
    )

if __name__ == "__main__":
    main()
