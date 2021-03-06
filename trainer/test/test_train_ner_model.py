from pathlib import Path
from data_manager.builder import NERDatasetBuilder
from model.sequence_tagger.bilstm_crf import BilstmCRF
from trainer.seq_tag_trainer import SequenceTaggingModelTrainer


def test_model_train_with_train_data():
    embedding_dim = 50
    hidden_dim = 50
    epochs = 400
    eval_steps = 10

    input_path = './trainer/test/test_dataset/ner/input.txt'
    label_path = './trainer/test/test_dataset/ner/output.txt'

    deploy_dir = Path('./trainer/test/test_dataset/ner/train_dataset')

    batch_size = 2
    sequence_length = 15

    ner_builder = NERDatasetBuilder(input_path, label_path, dataset_dir=deploy_dir / 'dataset')

    ner_builder.build_vocabulary()
    ner_builder.build_trainable_dataset()
    train_data_loader, valid_data_loader = ner_builder.build_data_loader(batch_size, sequence_length)

    word_to_idx, tag_to_idx = ner_builder.source_to_idx, ner_builder.target_to_idx

    ner_model = BilstmCRF(len(word_to_idx), tag_to_idx, embedding_dim, hidden_dim)

    ner_trainer = SequenceTaggingModelTrainer(train_data_loader,
                                              valid_data_loader,
                                              ner_model,
                                              epochs,
                                              eval_steps,
                                              deploy_path=deploy_dir / 'model')

    ner_trainer.train()

    assert ner_trainer.train_loss < 2
