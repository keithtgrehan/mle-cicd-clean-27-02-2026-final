# Intro to Data Version Control (DVC)

[**DVC**](https://dvc.org/) is a tool for **data versioning**, **data pipelines**, and **reproducibility**. It is naming itself open-source, Git-based data science. It is developed by _iterative.ai_. 

## Basic uses of DVC

DVC is used to organize your data and your code. It is a tool to version your data and your code, NOT your models (for this you can use MLflow).

You can use it to:
- **track and save data** the same way you capture code
- **compare model metrics** among experiments
- **adopt engineering tools and best practices** in data science projects

## Data versioning

DVC lets you capture the versions of your data and models in **Git commits** while storing them on-premises or in cloud storage, although it is not a storage solution. DVC also enables **cross-project reusability** of these data artifacts. This means that your projects can depend on data from other repositories — like a package management system for data science.

Let's try it out. We will use the Green Taxi data for January 2025:

```bash
wget -P ./data https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-01.parquet
```

Now we have to **initialize the DVC repository**:

```bash
dvc init
```

This will create a `.dvc` folder. 

You can add the local data to the DVC repository like this:

```bash
dvc add ./data/green_tripdata_2025-01.parquet
```

DVC stores information about the added file in a `.dvc` file named `data/green_tripdata_2025-01.parquet.dvc`. This small, human-readable **metadata file** acts as a placeholder for the original data for the purpose of Git tracking.

The output will tell you what to do next:

```bash
git add data/green_tripdata_2025-01.parquet.dvc
```

Now we can commit the changes:

```bash
git commit -m "Add data"
```

But we want to add a **remote storage**. We will use Google Cloud Storage (GCS) for this (you can use any other storage provider like AWS S3 or Azure Blob Storage). First create a **new bucket** in GCS. Then create a **service account** (with `Storage Admin` and `Storage Object Admin` roles) and download the JSON file. Then we can add the remote storage:


```bash
dvc remote add -d myremote gs://<bucket-name>/
```

And because we need to authenticate with GCS we need to add the credentials:

```bash
dvc remote modify --local myremote \
                    credentialpath 'path/to/project-XXX.json'
```
And commit the changes:

```bash
git commit .dvc/config  -m "Add remote storage"
```

And now you can **push the data** to the remote storage:

```bash
dvc push
```

You can now share the repository with your colleagues. They can clone the repository and **pull the data** from the remote storage with (of course they need to authenticate with GCS):

```bash
dvc pull
```

So in the end you only add the `.dvc` files to git and the data is stored in the remote storage and is still accessible for everyone. And if changes are made to the data you can just push and commit the changes to the remote storage and everyone can pull the changes.


## Pipelines

Versioning large data files and directories for data science is powerful, but often not enough. Data needs to be filtered, cleaned, and transformed before training ML models - for that purpose DVC introduces a **build system** to define, execute and track **data pipelines** — a series of **data processing stages**, that produce a final result.

If you want to read more about pipelines you can read the [documentation](https://dvc.org/doc/start/data-pipelines). We will not go into detail here.
