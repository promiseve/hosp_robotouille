import torch
from torch_geometric.nn import GCNConv
import torch.nn.functional as F
from torch_geometric.utils import dense_to_sparse

class GCNComm(torch.nn.Module):
    def __init__(self, input_shape, args, training=True):
        super(GCNComm, self).__init__()
        self.args = args
        self.training = training
        self.convs = []
        self.convs.append(GCNConv(input_shape, self.args.msg_hidden_dim))
        for i in range(1,self.args.num_layers-1):
            self.convs.append(GCNConv(self.args.msg_hidden_dim, self.args.msg_hidden_dim))
        self.convs.append(GCNConv(self.args.msg_hidden_dim, self.args.msg_out_size))    
    
    def cuda_transfer(self):
        for i in range(self.args.num_layers):
            self.convs[i].cuda()

    def forward(self, x, adj_matrix):
        # Ensure proper dimensions for adjacency matrix
        if len(adj_matrix.shape) == 2:
            adj_matrix = adj_matrix.unsqueeze(0)
        if len(x.shape) == 2:
            x = x.unsqueeze(0)

        x_out = []
        for x_in, am_in in zip(torch.unbind(x, dim=0), torch.unbind(adj_matrix, dim=0)):
            if x_in.dim() != 2:
                raise ValueError(f"Node features must have shape (num_nodes, num_features), got {x_in.shape}")
            if am_in.dim() != 2:
                raise ValueError(f"Each adjacency matrix must be 2D, got {am_in.shape}")

            for i in range(self.args.num_layers):
                sparse_adj = dense_to_sparse(am_in)
                x_in = self.convs[i](x_in, sparse_adj[0])  # Pass sparse adjacency to GCNConv
                if (i + 1) < self.args.num_layers:
                    x_in = F.elu(x_in)
                    x_in = F.dropout(x_in, p=0.2, training=self.training)
            x_out.append(x_in)

        return torch.stack(x_out, dim=0)






class GATComm(torch.nn.Module):
    def __init__(self, input_shape, args, training=True):
        super(GATComm, self).__init__()
        self.args = args

        self.convs = []
        self.convs.append(GCNConv(input_shape, self.args.msg_hidden_dim))
        for i in range(1,self.args.num_layers-1):
            self.convs.append(GCNConv(self.args.msg_hidden_dim, self.args.msg_hidden_dim))
        self.convs.append(GCNConv(self.args.msg_hidden_dim, self.args.msg_out_size))    
    