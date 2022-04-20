# starwars_explorer

## Possible improvements

 * Integrate Sentry for reporting errors (must-have for production)
 * Integrate tools like DataDog for gathering logs and metrics
 * Use structured logs (like `python-json-logger`)
 * Use external storage for files (object storage like S3, persitent volumes, maybe EBS)
 * Record log of downloading new dataset
 * Consider using some kind of a worker for moving as much as possible to background (Celery) if it would not fit into request time limit
 * Prevent users from starting multiple downloads at the same time
 * For testing views I would try to use tool like Cypress
 * Depending of the use case of the app it might be worth exposing API of some kind (REST, or GQL) and then use that API to implement fancy UI.
