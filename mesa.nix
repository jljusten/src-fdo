with import <nixpkgs> {};
mesa.overrideAttrs(
	oldAttrs : {
		buildInputs = [ meson ninja bison flex glslang ] ++
			      oldAttrs.buildInputs;
	}
)
