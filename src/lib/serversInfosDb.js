export const minecraftVersions = getMinecraftVersions();

function getMinecraftVersions() {
  let minecraftVersions = {}
  function getAvailableTypes(version) {
    const [major, minor] = version.split(".").map(Number);

    const availableTypes = ["vanilla"];

    if (major <= 1 || (major === 1 && minor <= 20)) {
      availableTypes.push("forge");
    }

    if (major === 1 && minor >= 7) {
      availableTypes.push("spigot");
    }

    if (major === 1 && minor >= 12) {
      availableTypes.push("paper");
    }
    return availableTypes;
  }

  function addPatchVersions(major, minor, patchMax) {
    for (let p = 0; p <= patchMax; p++) {
      const patch = p===0 ? "" : `.${p}`;
      const version = `1.${major}${patch}`;
      minecraftVersions[version] = {
        availableTypes: getAvailableTypes(version)
      };
    }
  }

  addPatchVersions(7, 0, 10);
  addPatchVersions(8, 0, 9);
  addPatchVersions(9, 0, 4);
  addPatchVersions(10, 0, 2);
  addPatchVersions(11, 0, 2);

  addPatchVersions(12, 0, 2);
  addPatchVersions(13, 0, 2);
  addPatchVersions(14, 0, 4);
  addPatchVersions(15, 0, 2);
  addPatchVersions(16, 0, 5);
  addPatchVersions(17, 0, 1);
  addPatchVersions(18, 0, 2);
  addPatchVersions(19, 0, 4);
  addPatchVersions(20, 0, 6);
  addPatchVersions(21, 0, 4);

  return minecraftVersions;
}