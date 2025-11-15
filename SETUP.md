# Set-Up the project

## 1. Requirements

- Docker
- Docker compose
- Git
- (Optional) Python 3.10+ if you plan to run Django locally without Docker

## 2. Clone the project

``` bash
git clone <REPOSITORY_URL>
cd critikon
```

## 3. Create your .env file

The project includes an example environment file called *.env.example.*

Copy it to create your real *.env*:

``` bash
cp .env.example .env
```

Open *.env* and update values if needed:

``` ini
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY=CHANGE_ME_TO_A_RANDOM_SECRET_KEY
DEBUG=True

UID=1000
GID=1000
```

**Important**:

* SECRET_KEY must be replaced with a random secure string (32+ chars).

* For development, default PostgreSQL credentials (postgres/postgres) are fine.

* Do not remove UID and GID unless you know what you're doing.

## 4. Configure domains (if deploying to a server)

If you plan to deploy using Traefik + HTTPS, open docker-compose.yml and replace:

```
yourdomain.com
app.yourdomain.com
media.yourdomain.com
```
with your real domain names.

Traefik will automatically generate Let's Encrypt SSL certificates.

If you’re running locally or don’t need HTTPS yet, you can skip this entire section.

## 5. Build and start the application

``` bash
docker compose up --build
```

This will:

1. Start PostgreSQL

2. Build the Django application container

3. Start the Traefik reverse proxy (if enabled)

4. Serve static/media files

5. Launch the app on your domain or local environment

## 6. Run database migrations

Once containers are up, run:

``` bash
docker compose exec web python manage.py migrate
```

Optionally create a superuser:

``` bash
docker compose exec web python manage.py createsuperuser
```

## 7. Collect static files (production only)

``` bash
docker compose exec web python manage.py collectstatic --noinput
```

## 8. Access the application

If running locally:

``` arduino
http://localhost
```

If running with Traefik + domain:

``` arduino
https://app.yourdomain.com
```

## 9. Useful commands

Rebuild the containers

``` bash
docker compose up --build
```
Stop the stack

``` bash
docker compose down
```
View logs

``` bash
docker compose logs -f
```
Open a shell inside Django container

``` bash
docker compose exec web bash
```