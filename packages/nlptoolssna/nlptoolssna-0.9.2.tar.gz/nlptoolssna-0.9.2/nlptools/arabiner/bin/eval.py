import os
import logging
from collections import namedtuple
from nlptools.arabiner.utils.helpers import load_checkpoint, make_output_dirs, logging_config
from nlptools.arabiner.utils.data import get_dataloaders, parse_conll_files
from nlptools.arabiner.utils.metrics import compute_single_label_metrics, compute_nested_metrics
from nlptools.DataDownload import downloader
logger = logging.getLogger(__name__)


def evaluate_dataset(output_path,data_paths ,batch_size=32):
    """
    Run the model to evaluate text data and save the predictions.

    Args:
        output_path (str): Path to save the results.
        model_path (str): Model path.
        data_paths (list[str]): List of paths to text or sequence files to tag.
        batch_size (int, optional): Batch size. Default is 32.
    """
    # Create directory to save predictions
    make_output_dirs(output_path, overwrite=True)
    logging_config(log_file=os.path.join(output_path, "eval.log"))
    filename = 'Wj27012000.tar'
    path =downloader.get_appdatadir()
    model_path = os.path.join(path, filename)
    # Load tagger
    tagger, tag_vocab, train_config = load_checkpoint(model_path)

    # Convert text to a tagger dataset and index the tokens in args.text
    datasets, vocab = parse_conll_files(data_paths)

    vocabs = namedtuple("Vocab", ["tags", "tokens"])
    vocab = vocabs(tokens=vocab.tokens, tags=tag_vocab)

    # From the datasets generate the dataloaders
    dataloaders = get_dataloaders(
        datasets, vocab,
        train_config.data_config,
        batch_size=batch_size,
        shuffle=[False] * len(datasets)
    )

    # Evaluate the model on each dataloader
    for dataloader, input_file in zip(dataloaders,data_paths):
        filename = os.path.basename(input_file)
        predictions_file = os.path.join(output_path, f"predictions_{filename}")
        _, segments, _, _ = tagger.eval(dataloader)
        tagger.segments_to_file(segments, predictions_file)

        if "Nested" in train_config.trainer_config["fn"]:
            compute_nested_metrics(segments, vocab.tags[1:])
        else:
            compute_single_label_metrics(segments)

