"""
tk_r_em network suites designed to restore different modalities of electron microscopy data

Author: Ivan Lobato
Email: Ivanlh20@gmail.com
"""
import os
import matplotlib
import numpy as np

# Check if running on remote SSH and use appropriate backend for matplotlib
remote_ssh = "SSH_CONNECTION" in os.environ
matplotlib.use('Agg' if remote_ssh else 'TkAgg')
import matplotlib.pyplot as plt

def fcn_set_gpu_id(gpu_visible_devices: str = "0") -> None:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_visible_devices

fcn_set_gpu_id("0")

from tk_r_em import load_network

def fcn_inference():
    """
    Perform inference on test data using a pre-trained model and visualize the results.
    """
    # select one of the available networks from [sfr_hrsem, sfr_lrsem, sfr_hrstem, sfr_lrstem, sfr_hrtem, sfr_lrtem]
    net_name = 'sfr_hrtem'
    
    # load experimental hrstem data
    x = np.load(os.path.join(os.getcwd(), 'test', 'q1_test2 (inverted).npy'))
        
    # load its corresponding model
    r_em_nn = load_network(net_name)
    r_em_nn.summary()

    batch_size = 8

    # run inference
    # y_p = r_em_nn.predict(x, batch_size)
    y_p = r_em_nn.predict_patch_based(x, patch_size=256, stride=128, batch_size=16)

    fig, axs = plt.subplots(2, 1, figsize=(48, 6))

    axs[0].imshow(x, cmap='hot')
    axs[0].set_xticks([])
    axs[0].set_yticks([])
    axs[0].grid(False)
    axs[0].set_ylabel(f"Experimental {net_name} image", fontsize=14, )

    axs[1].imshow(y_p, cmap='hot')
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].grid(False)
    axs[1].set_ylabel(f"Restored {net_name} image", fontsize=14)

    fig.subplots_adjust(hspace=2, wspace=10)
    fig.tight_layout()
    
    if remote_ssh:
        plt.savefig(f"restored_{net_name}.png", format='png')
    else:
        fig.show()

    print('Done')

if __name__ == '__main__':
    fcn_inference()