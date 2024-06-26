import logging
import time
import unittest

from AlgoTree.treenode import TreeNode
from AlgoTree.utils import visit

logging.basicConfig(level=logging.DEBUG)


class TestTreeNodeAdvanced(unittest.TestCase):
    def setUp(self):
        self.root = TreeNode(name="root", value="root_value")
        self.child1 = TreeNode(
            name="child1", parent=self.root, value="child1_value"
        )
        self.child2 = TreeNode(
            name="child2", parent=self.root, value="child2_value"
        )
        self.child1_1 = TreeNode(
            name="child1_1", parent=self.child1, value="child1_1_value"
        )
        self.child2_1 = TreeNode(
            name="child2_1", parent=self.child2, value="child2_1_value"
        )

        # tree looks like this:
        # root
        # ├── child1
        # │   └── child1_1
        # └── child2
        #     └── child2_1

    def test_move_subtree(self):
        new_parent = self.child2
        subtree_root = self.child1

        # Move subtree
        subtree_root.parent = new_parent
        # root
        # └── child2 (new_parent)
        #     ├── child2_1
        #     └── child1 (subtree_root)
        #         └── child1_1

        # Verify new structure
        self.assertEqual(subtree_root.parent, new_parent)
        self.assertIn(subtree_root, self.child2.children)
        self.assertNotIn(subtree_root, self.root.children)

    def test_cyclic_structure_detection(self):
        with self.assertRaises(ValueError):
            self.child1.parent = self.child1_1
            TreeNode.check_valid(self.root)

    def test_custom_payload_and_attributes(self):
        custom_node = TreeNode(
            name="custom", parent=self.root, custom_attr="custom_value"
        )
        self.assertEqual(custom_node.custom_attr, "custom_value")
        self.assertIn(custom_node, self.root.children)

    def test_large_tree_performance(self):
        # Create a large tree
        large_root = TreeNode(name="large_root")
        current_level = [large_root]
        for _ in range(5):  # Adjust depth as needed
            next_level = []
            for node in current_level:
                for i in range(10):  # Adjust branching factor as needed
                    next_level.append(TreeNode(name=f"node_{i}", parent=node))
            current_level = next_level

        # Measure traversal time
        start_time = time.time()
        visit(large_root, lambda n: False, order="pre")
        traversal_time = time.time() - start_time

        # Assert traversal time is within acceptable limits (e.g., 1 second)
        self.assertLess(traversal_time, 1)

    def test_edge_cases(self):
        empty_tree = TreeNode()
        single_node_tree = TreeNode(name="single")

        # Empty tree checks
        self.assertEqual(len(empty_tree.children), 0)
        self.assertIsNone(empty_tree.parent)

        # Single node tree checks
        self.assertEqual(len(single_node_tree.children), 0)
        self.assertIsNone(single_node_tree.parent)
        self.assertEqual(single_node_tree.name, "single")


if __name__ == "__main__":
    unittest.main()
