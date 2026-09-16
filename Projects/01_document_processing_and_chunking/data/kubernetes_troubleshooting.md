# Pod Pending Troubleshooting

Check the pod's scheduling events:

```sh
kubectl describe pod <pod-name> -n <namespace>
```

Look for insufficient CPU or memory, unmatched node selectors, node taints,
or persistent volume claims (PVCs) that have not bound to storage.

Check node capacity and PVC status before changing resource requests.

# CrashLoopBackOff

Inspect the previous container's logs:

```sh
kubectl logs <pod-name> -n <namespace> --previous
```

Check container exit codes, application configuration, and required secrets.
Use pod events to check whether a failing liveness probe caused restarts.

