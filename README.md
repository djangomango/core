# Core

### Dependencies:

Install Docker and Docker Compose:
   - Docker version 20.10.7+ and Docker Compose version 1.29.2+ are required.
   - For Ubuntu, refer to the following link: [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/).
   - If you're using Debian or Ubuntu, you can use the bash scripts in the `/helpers` directory to install Docker and Docker Compose:
     ```bash
     bash helpers/install_docker.sh
     bash helpers/install_docker_compose.sh
     ```

### Configuration:

1. Create Configuration Files:
   - Create the following files in the root directory:
     - `dev.env`
     - `prod.env`
     - `superusers.json`
   - Use the respective `*.dist` files as templates for these new files.

2. Generate Django Secret Key:
   - Visit [https://djecrety.ir/](https://djecrety.ir/) or any other suitable tool.
   - Generate a new Django secret key.

3. Set Django Secret Key:
   - Open `dev.env` and `prod.env` files.
   - Set the value of `DJANGO_SECRET_KEY` to the newly obtained secret key.

4. Set Admin Email and Site Name:
   - Open `dev.env` and `prod.env` files.
   - Set the value of `DJANGO_SITE_NAME` to the desired site name.
   - Set the value of `DJANGO_SITE_DOMAIN` to the desired site domain.
   - Set the value of `ADMIN_EMAIL` to the desired admin email address.

5. Set Allowed Hosts (for production environment):
   - Open the `prod.env` file.
   - Set the value of `DJANGO_ALLOWED_HOSTS` to the desired host address(es).
     - Example: `DJANGO_ALLOWED_HOSTS=example.com,www.example.com`

6. Set Database Password:
   - Open the `prod.env` file.
   - Set the value of `DB_PASSWORD` to the desired database password.

7. Set New Admin Account Credentials:
   - Open the `superusers.json` file.
   - Set a new email and password for the admin account in the JSON format.

8. Encrypt/ decrypt *.env/ superusers.json files (optional):
	```bash
	bash helpers/gpg_wrapper.sh -f *.env -e encrypt
	bash helpers/gpg_wrapper.sh -f *.env.gpg -e decrypt
	```

9. Update the included django utilities (optional):
	```bash
	git fetch https://github.com/buswedg/django-utils.git main
	git subtree pull --prefix=apps/utils https://github.com/buswedg/django-utils.git main --squash
	```


### Run:

- Run locally for development:
	```bash
	docker-compose -f docker-compose.dev.yml --env-file dev.env up
	```

- Run for production (without ssl):
	```bash
	docker-compose -f docker-compose.prod.yml --env-file prod.env up
	```

- Run for production (with ssl):
	```bash
	docker-compose -f docker-compose.prod.ssl.yml --env-file prod.env up
	```

- To recompile frontend app for production:
	```bash
	docker-compose -f docker-compose.frontend-build.yml run --rm node npm run prod
	```

- To rebuild email templates:
	```bash
	docker-compose -f docker-compose.frontend-build.yml run --rm node npm run maizzle:build
	```

- To recompile frontend, rebuild email templates, and deploy the app for production (with ssl):
	```bash
	bash deploy.sh
	```

- To analyze frontend app bundle:
	```bash
	docker-compose -f docker-compose.frontend-build.yml run node npm run profile
	docker-compose -f docker-compose.frontend-build.yml run node npm run analyzer -p 8000:8000
	```

To inspect emails sent by the app, browse to http://127.0.0.1:8025/