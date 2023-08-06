import torch
import torch.nn.functional as F


def compute_baseline_loss(advantages):
    return 0.5 * torch.mean(advantages**2)


def compute_entropy_loss(logits):
    policy = F.softmax(logits, dim=-1)
    log_policy = F.log_softmax(logits, dim=-1)
    entropy_per_timestep = torch.sum(-policy * log_policy, dim=-1)
    return -torch.mean(entropy_per_timestep)


def compute_policy_gradient_loss(logits, actions, advantages):
    cross_entropy = F.nll_loss(
        F.log_softmax(torch.flatten(logits, 0, 1), dim=-1),
        target=torch.flatten(actions, 0, 1),
        reduction="none",
    )
    cross_entropy = cross_entropy.view_as(advantages)
    policy_gradient_loss_per_timestep = cross_entropy * advantages.detach()
    return torch.mean(policy_gradient_loss_per_timestep)


# from https://github.com/facebookresearch/minihack/blob/65fc16f0f321b00552ca37db8e5f850cbd369ae5/minihack/agent/polybeast/models/losses.py
# NOTE: those functions do not divide by the batch size


def compute_forward_dynamics_loss(pred_next_emb, next_emb):
    forward_dynamics_loss = torch.norm(pred_next_emb - next_emb, dim=2, p=2)
    return torch.sum(torch.mean(forward_dynamics_loss, dim=1))


def compute_inverse_dynamics_loss(pred_actions, true_actions):
    inverse_dynamics_loss = F.cross_entropy(
        torch.flatten(pred_actions, 0, 1),
        torch.flatten(true_actions, 0, 1),
        reduction="none",
    )
    inverse_dynamics_loss = inverse_dynamics_loss.view_as(true_actions)
    return torch.sum(torch.mean(inverse_dynamics_loss, dim=1))
