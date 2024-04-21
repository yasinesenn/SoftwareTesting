from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from YazilimTest.forms import GitHubDepoForm
from .models import GitHubDepo, JavaClass

import YazilimTest.gitOperations
import YazilimTest.fileOperations

def github_depo_ekle(request):
    if request.method == 'POST':
        form = GitHubDepoForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            github_depo = GitHubDepo.objects.create(url=url)
            github_depo.save()
            
            javaModels = YazilimTest.fileOperations.read_Java_Files(github_depo,YazilimTest.gitOperations.clone_dir)
            return render(request, "index.html", {"javaModels": javaModels})
    else:
        form = GitHubDepoForm()  

    return render(request, 'getRepoURL.html', {'form': form})

def github_repo_list(request):
    github_repos = GitHubDepo.objects.all()
    return render(request, 'github_repo_list.html', {'github_repos': github_repos})

def java_class_list(request, github_repo_id):
    github_repo = get_object_or_404(GitHubDepo, pk=github_repo_id)
    java_classes = github_repo.javaclass_set.all()
    return render(request, 'index.html', {'github_repo': github_repo, 'javaModels': java_classes})



