# API Deployment

Example environment: staging. Deployment name: api.

Before deploying, confirm the Kubernetes context and that CI checks passed.
Record the currently deployed image tag and confirm the new image is available.

Update the api container to the approved image:

```sh
kubectl set image deployment/api api=<image>:<tag> -n staging
kubectl rollout status deployment/api -n staging --timeout=120s
```

Check readiness, application logs, and the API health endpoint.

# Rollback Procedure

If the release fails health checks, confirm the previous revision is safe
to restore, including compatibility with any database changes.

```sh
kubectl rollout undo deployment/api -n staging
kubectl rollout status deployment/api -n staging --timeout=120s
```

Verify API health and record the failed release and rollback in incident notes.

