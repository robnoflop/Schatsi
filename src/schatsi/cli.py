import click
import nltk


from schatsi.jobs import *

nltk.download("punkt")


@click.command()
@click.option('--input_path', help='The path where all files to process can be found.')
@click.option('--output_path', help='The path where results are put')
@click.option('--functional_terms', help='Path to a CSV with all funtional termns')
@click.option('--negative_terms', help='Path to a CSV with all negative termns')
@click.option('--parallel', default=True, help='Prallel processing or not')
def cli(input_path, output_path, functional_terms, negative_terms, parallel):
    if parallel:
        job = ParallelJob(input_path, output_path, functional_terms, negative_terms)
    else:
        job = SingleJob(input_path, output_path, functional_terms, negative_terms)
    
    job.process()

if __name__ == "__main__":
    job = ParallelJob("data/input", "data/output", "data/metadata/functional_terms.csv", "data/metadta/negative_terms.csv")
    job.process()
    
    