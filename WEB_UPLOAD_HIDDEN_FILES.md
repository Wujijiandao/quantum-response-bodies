# Hidden GitHub files

Browser drag-and-drop may omit dotfiles or dot-directories depending on how the upload is performed. The files are valid GitHub repository files and **can** be stored on GitHub.

Preferred method: use Git locally and push the repository.

If using the GitHub website, choose **Add file -> Create new file** and create these exact paths manually:

- `.gitignore`
- `.github/workflows/tests.yml`

For the workflow path, type `.github/workflows/tests.yml` as the filename; GitHub creates the intermediate directories. Copy the contents from this frozen package.
