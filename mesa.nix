# Jordan Justen : this file is public domain
with import <nixpkgs> {};
mesa.overrideAttrs(
	oldAttrs : {
		buildInputs = [ libclc spirv-llvm-translator spirv-tools ] ++
			      oldAttrs.buildInputs;
	}
)
