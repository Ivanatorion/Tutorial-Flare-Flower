from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator

import model

class GraphSearchShareableGenerator(ShareableGenerator):
    def learnable_to_shareable(self, learnable: model.GraphLearnable, fl_ctx: FLContext) -> Shareable:
        dxo = model.graph_learnable_to_dxo(learnable)
        return dxo.to_shareable()

    def shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> model.GraphLearnable:
        if not isinstance(shareable, Shareable):
            raise TypeError("shareable must be Shareable, but got {}.".format(type(shareable)))

        dxo = from_shareable(shareable)

        gl = model.make_graph_learnable(dxo.data["graph"], dxo.data["partition"])
        return gl