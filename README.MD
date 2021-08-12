# yet-another-artifactory-cleaner
## Descriprion
This script work with generic repo and structure looks like
```
repository-name
    path-for-cleaner
        build-1
            artifact.tar.gz
        build-2
            artifact.tar
        build-3
            artifact.gz
        develop
            build-4
                artifact.tar.gz
            build-5
                artifact.tar
    anather-path
    ...
```
and this script is deleting the folder in which the file is older than variable lower_date

### For build exec
workspace.sh build

### For run exec
workspace.sh run

### Config .env
```
dry_run=True # True - dry run process without deleting
artifactory_url="https://artifactory.domain.name"
token="secret"
repoKey="repository-name"
path="path-for-cleaner"
lower_date="01-01-2020" # %Y-%m-%d
```