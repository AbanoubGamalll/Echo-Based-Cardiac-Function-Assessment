import torch
import torch.nn as nn
from transformers import BertConfig, BertModel

from ResNetAE import ResNetAE


class TransformerModel(nn.Module):
    def __init__(self, embedding_dim=1024, num_hidden_layers=16, attention_heads=16, intermediate_size=8192,
                 input_shape=(128, 128, 3)):
        super(TransformerModel, self).__init__()

        # ResNet encoder
        self.model_AE = ResNetAE(input_shape=input_shape, n_ResidualBlock=8, n_levels=4,
                                 bottleneck_dim=embedding_dim)
        self.model_AE.decoder = None
        self.model_AE.fc2 = None

        # BertModel encoder
        configuration = BertConfig(
            vocab_size=1,  # Set to 0/None ?
            hidden_size=embedding_dim,  # Length of embeddings
            num_hidden_layers=num_hidden_layers,  # 16
            num_attention_heads=attention_heads,
            intermediate_size=intermediate_size,  # 8192
            hidden_act='gelu',
            hidden_dropout_prob=0.1,
            attention_probs_dropout_prob=0.1,
            max_position_embeddings=1024,  # 64 ?
            type_vocab_size=1,
            initializer_range=0.02,
            layer_norm_eps=1e-12,
            pad_token_id=0,
            gradient_checkpointing=False,
            position_embedding_type='absolute',
            use_cache=True)

        configuration.num_labels = 3

        self.model_Bert = BertModel(configuration).encoder

        self.embedding_dim = embedding_dim

        last_features = 3
        self.extremas = nn.Sequential(
            nn.Linear(in_features=embedding_dim, out_features=embedding_dim // 2, bias=True),
            nn.LayerNorm(embedding_dim // 2),
            nn.LeakyReLU(negative_slope=0.05, inplace=True),

            nn.Linear(in_features=embedding_dim // 2, out_features=embedding_dim // 4, bias=True),
            nn.LayerNorm(embedding_dim // 4),
            nn.LeakyReLU(negative_slope=0.05, inplace=True),

            nn.Linear(in_features=embedding_dim // 4, out_features=last_features, bias=True),
            nn.Tanh()
        )

    def forward(self, frames, nF):
        # (BxF) x C x H x W => (BxF) x Emb
        # Frame [128, 3, 128, 128]
        frames = self.model_AE.encode(frames).squeeze()
        # embeddings [128, 1024]
        # output_bert
        # B x F x Emb => AttHeads+1 x B x F x Emb
        frames = self.model_Bert(frames.view(-1, nF, self.embedding_dim), output_hidden_states=True)
        # AttHeads+1 x B x F x Emb => B x F x Emb
        frames = torch.stack(frames.hidden_states).mean(dim=0)
        # B x F x Emb => B x F x 1
        frames = self.extremas(frames)
        # classes_vec [1, 128, 3]
        return frames
