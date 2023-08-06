import importlib.metadata

# import pip
#
def _is_editable(dist: importlib.metadata.PathDistribution) -> bool:
    all_pth = [f for f in dist.files if f.name.endswith(".pth")]
    if len(all_pth) != 1:  # Might be edge case if >1, unsure if possible
        return False
    (pth_file,) = all_pth
    content = pth_file.read_text()
    if content.startswith("/"):  # TODO: To delete
        print(content)
    # Here, should check with github action path
    return content.startswith("/")


def find_module_name() -> str:
    dists = [dist for dist in importlib.metadata.distributions() if _is_editable(dist)]
    if len(dists) != 1:
        names = [d.name for d in dists]
        raise ValueError(
            f"Could not auto-infer the package name: {names}. Please open an issue."
        )
    (dist,) = dists
    return dist.name


def get_local_version() -> str:
    """Returns the local version."""
    return importlib.metadata.version(find_module_name())


def main():
    print(get_local_version())
    # for f in d.files:
    #     if f.name.endswith(".pth"):
    #         print(d.name, f)
    #         print(f.read_text())
    # dist.name
    #     # assert p.exists(), p
    #     print(d.name, d.files[-1])
    # d = importlib.metadata.distribution("epot_test")
    # # p = d.locate_file("")
    # # assert p.exists(), p
    # print(d.name, d.files)
    # for f in d.files:
    #     print(f)
    # p = d.locate_file("epot_test.pth")
    # print(p)
    # print(p.read_text())

    # pip_ = pip.main()
    # for pckg in pip_.get_installed_distributions():
    #     print(pckg.project_name, pckg)


if __name__ == "__main__":
    main()
