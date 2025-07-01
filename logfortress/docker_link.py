class DockerLink:
    def __init__(self, image_name):
        self.image_name = image_name

    def build_link(self):
        # Base URL for Docker Hub
        base_url = "https://hub.docker.com/r/"

        # Split the image name into repository and name
        # Example: `library/nginx:latest` will split into `library/nginx` and `latest`
        repo_name, _, tag = self.image_name.partition(":")

        # If the image is part of the official library and doesn't specify a repository
        if "/" not in repo_name:
            repo_name = "library/" + repo_name

        # Construct the full URL
        image_url = f"{base_url}{repo_name}"

        return image_url
