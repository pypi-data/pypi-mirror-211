import ggml


class GGMLInitParams:
    def __init__(self):
        self.mem_size = 0
        self.mem_buffer = None
        self.no_alloc = False
        self._params = ggml.ggml_init_params(
            self.mem_size,
            self.mem_buffer,
            self.no_alloc,
        )


DEFAULT_PARAMS = GGMLInitParams()


class GGMLContext:
    def __init__(self, params: GGMLInitParams = DEFAULT_PARAMS):
        self._ctx: ggml.ggml_context_p = ggml.ggml_init(params._params)

    def __del__(self):
        ggml.ggml_free(self._ctx)

    def used_mem(self) -> int:
        return ggml.ggml_used_mem(self._ctx)


DEFAULT_CONTEXT = GGMLContext()


class GGMLObject:
    pass


class GGMLTensor:
    pass


class GGMLCGraph:
    pass


class GGMLScratch:
    pass


class GGMLOptParamsAdam:
    pass


class GGMLOptParamsLbfgs:
    pass


class GGMLOptParams:
    pass
