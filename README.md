# CI/CD (GitHub Actions)

![tests](https://github.com/keithtgrehan/mle-cicd-clean-27-02-2026-final/actions/workflows/test.yml/badge.svg)
![format](https://github.com/keithtgrehan/mle-cicd-clean-27-02-2026-final/actions/workflows/black.yml/badge.svg)

# CI/CD (GitHub Actions)

This repo demonstrates:
- pytest on PRs and pushes
- black formatting checks via GitHub Actions

## DVC data remote

The default DVC remote is `gs://keith-dvc-1772193245/` (`myremote`).

To run `dvc pull` in CI or a fresh clone, provide GCS credentials:
- set `GOOGLE_APPLICATION_CREDENTIALS` to a service-account JSON key file path
- grant that service account read/write access to the bucket
