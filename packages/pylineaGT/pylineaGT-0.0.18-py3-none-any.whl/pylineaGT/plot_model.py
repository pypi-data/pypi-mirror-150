from readline import parse_and_bind
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy.stats import multivariate_normal
import torch
import numpy as np


def plot_assignments_init(model, df_m=None, clusts="init_cluster"):
    df_m = get_df(model)
    df_m = add_cluster(df_m, model.init_params["clusters"], name="init_cluster")

    params = model.init_params

    fig = plt.figure(constrained_layout=True, figsize=(20,20))

    gs = GridSpec(3, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, :])

    ax2 = plt.subplot(gs.new_subplotspec((1, 0), colspan=1))
    ax3 = plt.subplot(gs.new_subplotspec((1, 1), colspan=1))
    ax4 = plt.subplot(gs.new_subplotspec((1, 2), colspan=1))

    ax5 = plt.subplot(gs.new_subplotspec((2, 0), colspan=1))
    ax6 = plt.subplot(gs.new_subplotspec((2, 1), colspan=1))
    ax7 = plt.subplot(gs.new_subplotspec((2, 2), colspan=1))

    sns.barplot(x=[_ for _ in range(model.K)], y=model.init_params["weights"].detach().numpy(), ax=ax1)
    ax1.set_ylim(0,1)
    ax1.set_title(f"Final conditions, K={model.K}")

    density = compute_density(params, clusts)

    palette = generate_palette(N=len(df_m[clusts].unique()))
    print(len(palette))

    hue_val = clusts
    sns.scatterplot(data=df_m, x="cov_early", y="cov_mid", hue=hue_val, ax=ax2, palette=palette, legend=False)
    sns.scatterplot(data=df_m, x="cov_mid", y="cov_late", hue=hue_val, ax=ax3, palette=palette, legend=False)
    sns.scatterplot(data=df_m, x="cov_late", y="cov_early", hue=hue_val, ax=ax4, palette=palette, legend=False)

    sns.kdeplot(data=density, x="cov_early", y="cov_mid", hue=hue_val, ax=ax2, palette=palette, legend=False, bw_adjust=10, thresh=.2)
    sns.kdeplot(data=density, x="cov_mid", y="cov_late", hue=hue_val, ax=ax3, palette=palette, legend=False, bw_adjust=10, thresh=.2)
    sns.kdeplot(data=density, x="cov_late", y="cov_early", hue=hue_val, ax=ax4, palette=palette, legend=False, bw_adjust=10, thresh=.2)

    means = get_means(model, clusts)
    sns.scatterplot(data=means, x="cov_early", y="cov_mid", hue=hue_val, \
        ax=ax2, palette=palette, legend=False, marker="s", s=100)
    sns.scatterplot(data=means, x="cov_mid", y="cov_late", hue=hue_val, \
        ax=ax3, palette=palette, legend=False, marker="s", s=100)
    sns.scatterplot(data=means, x="cov_late", y="cov_early", hue=hue_val, \
        ax=ax4, palette=palette, legend=False, marker="s", s=100)




def plot_assignments_final(model, out_file=None, clusts="cluster"):
    df_m = get_df(model)
    df_m = add_cluster(df_m, model.params["clusters"], name="cluster")

    params = model.params

    fig = plt.figure(constrained_layout=True, figsize=(20,20))

    gs = GridSpec(3, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, :])

    ax2 = plt.subplot(gs.new_subplotspec((1, 0), colspan=1))
    ax3 = plt.subplot(gs.new_subplotspec((1, 1), colspan=1))
    ax4 = plt.subplot(gs.new_subplotspec((1, 2), colspan=1))

    ax5 = plt.subplot(gs.new_subplotspec((2, 0), colspan=1))
    ax6 = plt.subplot(gs.new_subplotspec((2, 1), colspan=1))
    ax7 = plt.subplot(gs.new_subplotspec((2, 2), colspan=1))

    if model is not None:
        sns.barplot(x=[_ for _ in range(model.K)], y=model.params["weights"].detach().numpy(), ax=ax1)
        ax1.set_ylim(0,1)
        ax1.set_title(f"Final conditions, K={model.K}")

    density = compute_density(params, clusts)

    palette = generate_palette(N=len(df_m[clusts].unique()))
    print(len(palette))

    hue_val = clusts
    for k in df_m[clusts].unique():
        sns.kdeplot(data=density[density[clusts]==k], x="cov_early", y="cov_mid", hue=hue_val, \
            ax=ax2, palette=[palette[k]], legend=False, levels=20)
        sns.kdeplot(data=density[density[clusts]==k], x="cov_mid", y="cov_late", hue=hue_val, \
            ax=ax3, palette=[palette[k]], legend=False, levels=20)
        sns.kdeplot(data=density[density[clusts]==k], x="cov_late", y="cov_early", hue=hue_val, \
            ax=ax4, palette=[palette[k]], legend=False, levels=20)

    sns.scatterplot(data=df_m, x="cov_early", y="cov_mid", hue=hue_val, ax=ax2, palette=palette, legend=False)
    sns.scatterplot(data=df_m, x="cov_mid", y="cov_late", hue=hue_val, ax=ax3, palette=palette, legend=False)
    sns.scatterplot(data=df_m, x="cov_late", y="cov_early", hue=hue_val, ax=ax4, palette=palette, legend=False)

    means = get_means(model, clusts)
    sns.scatterplot(data=means, x="cov_early", y="cov_mid", hue=hue_val, \
        ax=ax2, palette=palette, legend=False, marker="s", s=100)
    sns.scatterplot(data=means, x="cov_mid", y="cov_late", hue=hue_val, \
        ax=ax3, palette=palette, legend=False, marker="s", s=100)
    sns.scatterplot(data=means, x="cov_late", y="cov_early", hue=hue_val, \
        ax=ax4, palette=palette, legend=False, marker="s", s=100)


    # sns.histplot(df_m[df_m["cov_early"]>5], x="cov_early", hue=hue_val, cbar=False, \
    #     ax=ax5, multiple="layer", edgecolor="white", bins=100, palette=palette)
    # sns.histplot(df_m[df_m["cov_mid"]>5], x="cov_mid", hue=hue_val, cbar=False, \
    #     ax=ax6, multiple="layer", edgecolor="white", bins=100, palette=palette)
    # sns.histplot(df_m[df_m["cov_late"]>5], x="cov_late", hue=hue_val, cbar=False, \
    #     ax=ax7, multiple="layer", edgecolor="white", bins=100, palette=palette)


def get_means(model, clusts):
    if clusts == "cluster":
        df = pd.DataFrame(model.params["mean"].detach().numpy()[:,:3], columns=["cov_early", "cov_mid", "cov_late"])
    if clusts == "init_cluster":
        df = pd.DataFrame(model.init_params["mean"].detach().numpy()[:,:3], columns=["cov_early", "cov_mid", "cov_late"])
    df["cluster"] = df.index

    return df


def generate_palette(N):
    return sns.color_palette("husl", N)


def compute_density(params, clust):
    dens = pd.DataFrame(columns=["cov_early", "cov_mid", "cov_late", clust])
    for k in range(params["K"]):
        # Generating a Gaussian bivariate distribution
        # with given mean and covariance matrix
        sigma = torch.mm(params["sigma"][k][:3], params["sigma"][k][:3].transpose(dim0=1, dim1=0))
        # sigma = params["sigma"]
        distr = multivariate_normal(cov=sigma.detach().numpy(), \
            mean=params["mean"][:,:3].detach().numpy()[k])
        data = distr.rvs(size=200)
        data = pd.DataFrame(data, columns=["cov_early", "cov_mid", "cov_late"])
        data[clust] = k
        data[clust] = data[clust].astype("category")
        dens = dens.append(data, ignore_index=True)
    return dens



def get_df(model):
    return pd.DataFrame(model.dataset.numpy()[:,:3], columns=["cov_early", "cov_mid", "cov_late"])


def add_cluster(df, clusters, name="cluster"):
    df[name] = clusters
    df[name] = df[name].astype("category")
    return df


def plot_loss_grads(model, save=False, out_file=None):
    fig = plt.figure(constrained_layout=True, figsize=(20,20))

    gs = GridSpec(4, 2, figure=fig)
    ax1 = plt.subplot(gs.new_subplotspec((0, 0), rowspan=1, colspan=2))
    ax2 = plt.subplot(gs.new_subplotspec((1, 0), rowspan=1, colspan=2))
    ax3 = plt.subplot(gs.new_subplotspec((2, 0), rowspan=1, colspan=2))

    ax4 = plt.subplot(gs.new_subplotspec((3, 0), colspan=2))

    ax1.plot(model.losses_grad_train["losses"])
    ax1.set_title(f"Train, K={model.K}")
    grad = list(model.losses_grad_train["gradients"].items())
    ax2.plot(grad[1][1], label=grad[1][0])
    ax2.legend(loc="best")
    ax3.plot(grad[2][1], label=grad[2][0])
    ax3.legend(loc="best")
    ax4.plot(grad[3][1], label=grad[3][0])
    ax4.legend(loc="best")

    # sns.lineplot(x=[_ for _ in range(model._n_iter)], y=model.params_train["nll"], ax=ax4) 
    # ax4.set_title(f"NLL, K={model.K}")
    # sns.lineplot(x=[_ for _ in range(model._n_iter)], y=model.params_train["entropy"], ax=ax5) 
    # ax5.set_title(f"Entropy, K={model.K}")

    if save:
        plt.savefig(out_file)