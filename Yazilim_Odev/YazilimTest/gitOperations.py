import os
from git import Repo,rmtree

# Klonlanacak dizin
clone_dir = "./repo_klonu"


def clean_clone_directory(directory): # Klonlanan repo klasorunu temizler.
    try:
        rmtree(directory)
        print(f"'{directory}' klasörü temizlendi.")
    except FileNotFoundError:
        print(f"'{directory}' klasörü bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def get_git_repository(repo_url): # Git deposundaki bilgileri alir.
   
    print(repo_url + " klonlaniyor...")
    repo = Repo.clone_from(repo_url, clone_dir)
    print("Klonlandı!")

    java_files = []
    for root, dirs, files in os.walk(clone_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))

    if java_files:
        print("Bulunan Java dosyaları:")
        for java_file in java_files:
            print(java_file)
    else:
        print("Java dosyası bulunamadı.")
    



def allOperations(repo_url):
    clean_clone_directory(clone_dir)
    get_git_repository(repo_url)
    







    