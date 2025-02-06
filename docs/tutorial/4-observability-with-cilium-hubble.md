# Tutorial 4: Observability with cilium hubble

> [!NOTE]
>
> This tutorial is work in progress.

If you run your application simulation on kubernetes you can use [cilium Hubble's ui](https://github.com/cilium/hubble).

Follow the instructions to install [cilium](https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/) and [enable the Hubble UI](https://docs.cilium.io/en/stable/observability/hubble/hubble-ui/#hubble-ui).

If you already have deployed your application simulation in a previous tutorial (for example the [two services from tutorial 1](./1-two-services.md)), you can navigate to `http://localhost:12000/?namespace=app-sim-tutorial1`
in your browser, and you will see the interaction between the load generator, and the two services.
