# The MIT License (MIT)
# Copyright © 2021 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Utils for checkpointing and saving the model.
import torch
import wandb
import copy
import bittensor as bt

def should_checkpoint( self ):
    # Check if enough epoch blocks have elapsed since the last checkpoint.
    return self.subtensor.block % self.config.neuron.checkpoint_block_length == 0

def checkpoint( self ):
    """ Checkpoints the training process."""
    bt.logging.info('checkpoint()')
    resync_metagraph( self )
    save_state( self )                    

def resync_metagraph( self ):
    """ Resyncs the metagraph and updates the hotkeys and moving averages based on the new metagraph. """
    bt.logging.info('resync_metagraph()')

    # Copies state of metagraph before syncing.
    previous_metagraph = copy.deepcopy( self.metagraph )

    # Sync the metagraph.
    self.metagraph.sync()

    # Creates a dictionary of uids and hotkeys from the previous metagraph state.
    uids_hotkeys_state_dict = dict( zip( previous_metagraph.uids.tolist(), previous_metagraph.hotkeys ) )

    # Creates a dictionary of latest uids and hotkeys of the metagraph.
    latest_uids_hotkeys_state_dict = dict( zip( self.metagraph.uids.tolist(), self.metagraph.hotkeys ) )

    if uids_hotkeys_state_dict != latest_uids_hotkeys_state_dict:
        bt.logging.info('Metagraph updated, re-syncing hotkeys, dendrite pool and moving averages')
        # Reconstruct the dendrite pool with the new endpoints.
        self.dendrite_pool.resync(self.metagraph)

        # Zero out all hotkeys that have been replaced.
        for uid, hotkey in enumerate( self.hotkeys ):
            if hotkey != self.metagraph.hotkeys[ uid ]:
                self.moving_averaged_scores[ uid ] = 0 #hotkey has been replaced

        # Check to see if the metagraph has changed size.
        # If so, we need to add new hotkeys and moving averages.
        if len(self.hotkeys) < len(self.metagraph.hotkeys):
            # Update the size of the moving average scores.
            new_moving_average = torch.zeros((self.metagraph.n)).to( self.device )
            new_moving_average[:len(self.hotkeys)] = self.moving_averaged_scores
            self.moving_averaged_scores = new_moving_average

        # Resize the gating model.
        bt.logging.info('Re-syncing gating model')
        self.gating_model.resync( previous_metagraph, self.metagraph )

        # Update the hotkeys.
        self.hotkeys = copy.deepcopy(self.metagraph.hotkeys)

def resync_linear_layer(
        linear_layer: torch.nn.Module,
        previous_metagraph: 'bt.metagraph.Metagraph',
        metagraph: 'bt.metagraph.Metagraph'
    ):
    """Resync the linear layer with the latest state of the network
       Args:
            linear_layer (:obj: torch.nn.Module): Linear layer to be resynced
            previous_metagraph (:obj: bt.metagraph.Metagraph):
                Previous state of metagraph before updated resync
            metagraph (:obj: bt.metagraph.Metagraph):
                Latest state of the metagraph with updated uids and hotkeys
    """
    uids_hotkeys_state_dict = dict(zip(previous_metagraph.uids.tolist(), previous_metagraph.hotkeys))
    latest_uids_hotkeys_state_dict = dict(zip(metagraph.uids.tolist(), metagraph.hotkeys))

    updated_uids_indices = []
    for uid, latest_hotkey in latest_uids_hotkeys_state_dict.items():
        if uids_hotkeys_state_dict.get(uid) != latest_hotkey:
            updated_uids_indices.append(uid)

    for index in updated_uids_indices:
        # Reinitialize the bias of the selected index of the linear layer
        torch.nn.init.zeros_(linear_layer.bias[index])
        # Clone the weights of the selected index of the linear layer
        weights = linear_layer.weight[index].clone()
        # Adds a dimension to the weights tensor to make it compatible with the xavier_uniform_ function
        torch.nn.init.xavier_uniform_(weights.unsqueeze(0))
        reinitialized_weights = weights.squeeze(0)
        # Copy the reinitialized weights back to the selected index of the linear layer
        linear_layer.weight[index].data.copy_(reinitialized_weights)

def save_state( self ):
    r""" Save hotkeys, gating model, neuron model and moving average scores to filesystem. """
    bt.logging.info('save_state()')
    try:
        neuron_state_dict = {
            'neuron_weights': self.moving_averaged_scores,
            'neuron_hotkeys': self.hotkeys
        }
        torch.save(neuron_state_dict, f'{self.config.neuron.full_path}/model.torch')
        bt.logging.success( prefix = 'Saved model', sufix = f'<blue>{ self.config.neuron.full_path }/model.torch</blue>' )

        # Save the gating model.
        gating_model_linear_layer_dict = self.gating_model.linear.state_dict()
        gating_model_name = self.config.gating.model_name.replace( '/', '_' )
        gating_model_file_path = f'{self.config.neuron.full_path}/{gating_model_name}_gating_linear_layer.pth'
        torch.save( gating_model_linear_layer_dict, gating_model_file_path )

        if not self.config.wandb.off:
            model_artifact = wandb.Artifact( f'{gating_model_name}_gating_linear_layer', type = 'model' )
            model_artifact.add_file( gating_model_file_path )
            self.wandb.log_artifact( model_artifact )            

        bt.logging.success(prefix='Saved gating model', sufix=f'<blue>{gating_model_file_path}</blue>')
    except Exception as e:
        bt.logging.warning( f'Failed to save model with error: {e}' )

def load_state( self ):
    r""" Load hotkeys and moving average scores from filesystem. """
    bt.logging.info('load_state()')
    try:
        state_dict = torch.load(f'{self.config.neuron.full_path}/model.torch')
        self.moving_averaged_scores = state_dict['neuron_weights'].clone().detach()
        self.hotkeys = state_dict['neuron_hotkeys']
        bt.logging.success( prefix = 'Reloaded model', sufix = f'<blue>{ self.config.neuron.full_path }/model.torch</blue>' )
    except Exception as e:
        bt.logging.warning( f'Failed to load model with error: {e}')

