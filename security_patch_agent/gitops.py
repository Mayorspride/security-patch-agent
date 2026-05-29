from pathlib import Path
from typing import Optional
from git import Repo, InvalidGitRepositoryError

class GitOperations:
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)
        try:
            self.repo = Repo(self.repo_path)
        except InvalidGitRepositoryError:
            self.repo = Repo.init(self.repo_path)

    def ensure_branch(self, branch_name: str) -> str:
        if self.repo.is_dirty(untracked_files=True):
            # keep user work safe; do not overwrite or stash silently
            pass
        current_names = [h.name for h in self.repo.heads]
        if branch_name in current_names:
            self.repo.git.checkout(branch_name)
        else:
            self.repo.git.checkout("-b", branch_name)
        return branch_name

    def diff(self) -> str:
        return self.repo.git.diff("--", ".")

    def commit_if_requested(self, message: str) -> Optional[str]:
        if not self.repo.is_dirty(untracked_files=True):
            return None
        self.repo.git.add(A=True)
        self.repo.index.commit(message)
        return self.repo.head.commit.hexsha
