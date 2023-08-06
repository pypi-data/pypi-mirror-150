from cartesio.core.decoder import GenomeToCode


class GenomeToPython(GenomeToCode):
    def __init__(self, metadata, function_set, use_catalog=True):
        super().__init__(metadata, function_set)
        self.indent = " " * 4
        self.use_catalog = use_catalog
        if self.use_catalog:
            self.import_catalog = (
                "from cartesio.image.catalog import Catalog2D as catalog"
            )

    def to_code(self, node_name, genome):
        python_code = ""
        if self.use_catalog:
            python_code += f"{self.import_catalog}\n\n"
            python_code += f"def {node_name}(image):\n"
            for i in range(self.shape.outputs):
                active_nodes = self.read_active_nodes(genome)[i]
                for node in active_nodes:
                    if node < self.shape.inputs:
                        python_code += f"{self.indent}channel_{node} = image[{node}]\n"
                    elif node < self.shape.out_idx:
                        function_index = self.read_function(
                            genome, node - self.shape.inputs
                        )
                        active_connections = self.function_set.arity_of(function_index)
                        connections = self.read_active_connections(
                            genome, node - self.shape.inputs, active_connections
                        )
                        parameters = self.read_parameters(
                            genome, node - self.shape.inputs
                        )
                        f_name = self.function_set.name_of(function_index)
                        c_names = [
                            f"channel_{c}" if c < self.shape.inputs else f"node_{c}"
                            for c in connections
                        ]
                        c_names = "[" + ", ".join(c_names) + "]"
                        python_code += f'{self.indent}node_{node} = catalog.get("{f_name}")({c_names}, {list(parameters)})\n'
                python_code += f"{self.indent}output_{i} = node_{node}\n"
                python_code += f"{self.indent}return output\n"
        print(python_code)
