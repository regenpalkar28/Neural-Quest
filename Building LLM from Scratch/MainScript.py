import torch
import torch.nn as nn
from torch.nn import functional as F
import os


device = 'cuda' if torch.cuda.is_available() else 'cpu'

# print(device)
checkpoint_dir = "model_checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

best_model_path = "model_checkpoints/best_model.pth"

dropout = 0.2
block_size = 128
n_embd = 384
n_head = 8 #how many heads are running in parallel
n_layer = 8 # no. of decoder blocks


allowed_chars = ['\n', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

chars =  sorted(allowed_chars)
vocab_size=len(chars)


#mapping from strings to integers
string_to_integer = {ch:i for i,ch in enumerate(chars) }
#mapping from integers to strings
integer_to_string = {i:ch for i, ch in enumerate(chars) }

encode = lambda s: [string_to_integer[c] for c in s]
decode = lambda l: ''.join([integer_to_string[i] for i in l])


class Block(nn.Module):

    def __init__(self, n_embd, n_head):
        super().__init__()
        #n_embed is dim(embedding)
        #n_head is number of heads
        head_size = n_embd // n_head
        # head_size is number of features each head will be capturing in multi head attention
        self.sa = MultiHeadAttention(n_head, head_size)
        # sa = SelfAttention
        self.ffwd = FeedForward(n_embd)
        # Feed Forward : Linear -> ReLU -> Linear
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)
        # these are just for prenorm and postnorm respectively.

    def forward(self, x):
        y = self.sa(x)
        x = self.ln1(x+y)
        y = self.ffwd(x)
        x = self.ln2(x+y)
        #self attention -> add a norm -> feed forward -> add a norm
        
        return x  
    
class FeedForward(nn.Module):

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential (
            nn.Linear(n_embd, 4*n_embd),
            nn.ReLU(),
            nn.Linear(4*n_embd, n_embd),
            nn.Dropout(dropout),
        )
    def forward(self,x):
        return self.net(x)  
    
class MultiHeadAttention(nn.Module):

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(head_size*num_heads, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out
    
class Head(nn.Module):

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias = False)
        self.query = nn.Linear(n_embd, head_size, bias = False)
        self.value = nn.Linear(n_embd, head_size, bias = False)
        self.register_buffer('tril' , torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)

    def forward(self,x):
        B,T,C = x.shape
        k = self.key(x)   # (B, T, head_size)
        q = self.query(x) # (B, T, head_size)

        # computing attention scores
        wei= q @ k.transpose(-2,-1)*k.shape[-1]**-0.5 
        # (B, t, head_size) @ (B, head_size, T) -> (B, T, T) 
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) #(B,T,T)
        wei = F.softmax(wei, dim=-1) # (B,T,T)
        wei = self.dropout(wei)

        # performing weighted aggregation of values
        v = self.value(x) #(B, T, head_size)
        out = wei @ v 
        # (B,T,T) @ (B, T, head_size) -> (B, T, head_size)
        return out
    
class GPTLM(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd) #norm of final layer
        self.lm_head = nn.Linear(n_embd, vocab_size)

        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            
    def forward(self, index, targets=None):
        B,T = index.shape
        token_emb = self.token_embedding_table(index)
        posn_emb = self.position_embedding_table(torch.arange(T, device=device))

        x = token_emb + posn_emb 
        x = self.blocks(x)
        x= self.ln_f(x)
        logits = self.lm_head(x)
        if targets==None:
            loss = None
        else:
            # batches, time, channels
            B, T, C = logits.shape
            #.view helps us to make a tensor with those dimensions
            logits = logits.view(B*T,C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        return logits, loss

    def generate(self, index, max_new_tokens):
        # index is a (B,T) array of indices in the present context
        for _ in range(max_new_tokens):
            index_cond = index[:, -block_size:]
            # retrive the predictions
            logits, loss = self.forward(index_cond)
            # focus on the last time-step
            logits = logits[:,-1,:] # (B,C)
            # apply softmax on logits to get the probabilities
            probs = F.softmax(logits, dim= -1) # (B,C)
            # sample from the distribution
            index_next = torch.multinomial(probs, num_samples = 1) # (B,1)
            index = torch.cat((index, index_next), dim=1) # (B,T+1)
        return index

model = GPTLM(vocab_size).to(device)
state_dict = torch.load(best_model_path, map_location=device)

model.eval()  # set to evaluation mode
own_state = model.state_dict()
for name, param in state_dict.items():
    if name in own_state and own_state[name].shape == param.shape:
        own_state[name].copy_(param)
print("Loaded best-model from Drive")

while True:
    prompt = input("Prompt (type 'exit' to end) : ")
    if prompt.lower() == 'exit':
        print("Exiting the program.")
        break
    context = torch.tensor(encode(prompt), dtype=torch.long, device=device)
    generated_chars = decode(model.generate(context.unsqueeze(0), max_new_tokens=500)[0].tolist())
    print(f'Completion:\n{generated_chars}')
