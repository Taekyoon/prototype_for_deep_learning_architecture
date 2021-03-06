from model.sequence_tagger.bilstm_crf import BilstmCRF
from model.sequence_tagger.cnn_bilstm_crf import CNNBilstmCRF
from model.sequence_tagger.transformer import TransformerTagger
from model.sequence_tagger.transformer import TransformerCRF
from model.sequence_tagger.bert import BertTagger

from model.joint_classifier_and_sequence_tagger.cnn_bilstm_crf import CNNBilstmCRF as CNNBilstmCRF_SLU
from model.joint_classifier_and_sequence_tagger.bilstm_crf import BilstmCRF as BilstmCRF_SLU
from model.joint_classifier_and_sequence_tagger.bert import BertJointTaggerAndClassifier

from model.seq2seq.bi_lstm_seq2seq import BiLSTMEncoder, LSTMDecoder, BiLSTMSeq2Seq
from model.modules.attention import LuongAttention

from pytorch_pretrained_bert.modeling import BertConfig


def create_model(type, tag_to_idx, model_configs):
    model_type = model_configs['type']
    model_params = model_configs['parameters']
    if type == 'ner' or type == 'word_segment':
        vocab_size = model_configs['vocab_size']
        if model_type == 'bilstm_crf':
            model = BilstmCRF(vocab_size, tag_to_idx, model_params['word_embedding_dims'],
                              model_params['hidden_dims'])
        elif model_type == 'cnn_bilstm_crf':
            model = CNNBilstmCRF(vocab_size, tag_to_idx, model_params['word_embedding_dims'],
                                 model_params['channel_dims'], model_params['conv_configs'],
                                 model_params['hidden_dims'])
        elif model_type == 'transformer':
            model = TransformerTagger(vocab_size, len(tag_to_idx), model_params['word_embedding_dims'],
                                      model_params['hidden_dims'], model_params['head_size'],
                                      model_params['layer_size'])
        elif model_type == 'transformer_crf':
            model = TransformerCRF(vocab_size, tag_to_idx, model_params['word_embedding_dims'],
                                   model_params['hidden_dims'], model_params['head_size'],
                                   model_params['layer_size'])
        elif model_type == 'bert':
            bert_configs = BertConfig(model_params['config_path'])
            model = BertTagger(bert_configs, len(tag_to_idx))
        else:
            raise ValueError()
    elif type == 'slu':
        vocab_size, class_size = model_configs['vocab_size'], model_configs['class_size']

        # num_layers = model_params['lstm_num_layers'] if 'lstm_num_layers' in model_params else 1
        # dropout = model_params['lstm_dropout'] if 'lstm_dropout' in model_params else 0.5

        if model_type == 'bilstm_crf':
            model = BilstmCRF_SLU(vocab_size, class_size, tag_to_idx, model_params['word_embedding_dims'],
                                  model_params['hidden_dims'])
        elif model_type == 'cnn_bilstm_crf':
            model = CNNBilstmCRF_SLU(vocab_size, class_size, tag_to_idx, model_params['word_embedding_dims'],
                                     model_params['channel_dims'], model_params['conv_configs'],
                                     model_params['hidden_dims'])
        elif model_type == 'bert':
            bert_configs = BertConfig(model_params['config_path'])
            model = BertJointTaggerAndClassifier(bert_configs, class_size, len(tag_to_idx))
        else:
            raise ValueError()
    elif type == 'translate':
        input_size, target_size = model_configs['source_size'], model_configs['target_size']
        if model_type == 'bilstm_seq2seq':
            encoder = BiLSTMEncoder(input_size, model_params['word_embedding_dims'], model_params['hidden_dims'])
            decoder = LSTMDecoder(target_size, model_params['word_embedding_dims'], model_params['hidden_dims'] ,
                                  model_params['hidden_dims'])
            model = BiLSTMSeq2Seq(encoder, decoder)
        elif model_type == 'bilstm_attn_seq2seq':
            encoder = BiLSTMEncoder(input_size, model_params['word_embedding_dims'], model_params['hidden_dims'])
            decoder = LSTMDecoder(target_size, model_params['word_embedding_dims'], model_params['hidden_dims'],
                                  model_params['hidden_dims'])
            attention = LuongAttention(model_params['hidden_dims'], model_params['hidden_dims'] * 2)
            model = BiLSTMSeq2Seq(encoder, decoder, attention=attention)
    else:
        raise ValueError()

    return model
