import torch

# Load the .th file
model_data = torch.load('/home/poe6/hosp_robotouille/results/models/qmix_seed677336568_None_2024-06-11 01:58:41.601187/100/opt.th', map_location=torch.device('cpu'))

# Inspect the contents
print(model_data)

# #use PyTorch's state_dict() method on the loaded model to see the structure and parameter shapes
# for param_tensor in model_data.state_dict():
#     print(param_tensor, "\t", model_data.state_dict()[param_tensor].size(), map_location=torch.device('cpu'))

# #convert the tensors to numpy arrays and print 
# for param_tensor in model_data.state_dict():
#     print(param_tensor, "\t", model_data.state_dict()[param_tensor].numpy(), map_location=torch.device('cpu'))

# Print the keys in the model_data dictionary
print("Keys in the model:")
for key in model_data.keys():
    print(key)

# If model_data is a state_dict, print the shape of each parameter
if isinstance(model_data, dict):
    for key, value in model_data.items():
        if isinstance(value, torch.Tensor):
            print(f"{key}: {value.shape}")

# Inspect the contents
print("\nFull model data:")
print(model_data)