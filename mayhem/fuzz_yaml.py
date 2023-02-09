#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=['strictyaml']):
    import strictyaml


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test = fdp.ConsumeIntInRange(0, 2)
    try:
        if test == 0:
            strictyaml.load(fdp.ConsumeRemainingString()).data
        elif test == 1:
            obj = strictyaml.load(fdp.ConsumeRemainingString())
            obj.as_yaml()
        elif test == 2:
            fuzz_dict = fuzz_helpers.build_fuzz_dict(fdp, [str, str])
            strictyaml.as_document(fuzz_dict).as_yaml()
    except strictyaml.YAMLError:
        return -1
    except AttributeError as e:
        if 'context_mark' in str(e):
            return -1
        raise


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
