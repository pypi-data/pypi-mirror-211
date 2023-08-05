#include <iostream>
#include <stdlib.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using Node = int64_t;
using Nodes = std::vector<Node>;
using GraphNeighbors = std::vector<Nodes>;
using Weight = float;
using Weights = std::vector<Weight>;
using GraphWeights = std::vector<Weights>;
using WeightMap = std::unordered_map<Node, Weight>;
using NodeSet = std::unordered_set<Node>;

bool sort_by_increase(
    const std::tuple<Node, Node, Node, float, Weight, Weight> &a,
    const std::tuple<Node, Node, Node, float, Weight, Weight> &b)
{
    return (std::get<2>(a) > std::get<2>(b));
}

std::tuple<Nodes, Weights, Weights, Weights, Weights, float> init_status(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights)
{
    size_t n_nodes = graph_neighbors.size();

    Nodes node2com;
    Weights internals;
    Weights loops;
    Weights degrees;
    Weights gdegrees;
    node2com.resize(n_nodes);
    internals.resize(n_nodes);
    loops.resize(n_nodes);
    degrees.resize(n_nodes);
    gdegrees.resize(n_nodes);

    float total_weight = 0;
    for (Node node = 0; node < n_nodes; node++)
    {
        node2com[node] = node;
        internals[node] = 0;
        loops[node] = 0;
        degrees[node] = 0;
        gdegrees[node] = 0;

        Nodes neighbors = graph_neighbors[node];
        Weights neighbors_weight = graph_weights[node];
        for (size_t i = 0; i < neighbors.size(); i++)
        {
            Node neighbor = neighbors[i];
            Weight weight = neighbors_weight[i];
            // if (neighbor == node)
            // {
            //     internals[node] += weight;
            //     loops[node] += weight;
            //     weight *= 2;
            // }
            // degrees[node] += weight;
            // gdegrees[node] += weight;
            // total_weight += weight;
            if (neighbor == node)
            {
                internals[node] += weight;
                loops[node] += weight;
                degrees[node] += 2 * weight;
                gdegrees[node] += 2 * weight;
                total_weight += 2 * weight;
            }
            else
            {
                degrees[node] += weight;
                gdegrees[node] += weight;
                total_weight += weight;
            }
        }
    }
    total_weight /= 2;
    return std::make_tuple(
        node2com,
        internals,
        loops,
        degrees,
        gdegrees,
        total_weight);
}

float modularity(
    Weights const &internals,
    Weights const &degrees,
    float total_weight,
    float resolution)
{
    float result = 0;
    float m = 2. * total_weight;
    for (Node com = 0; com < degrees.size(); com++)
    {
        result += resolution * internals[com] / total_weight;
        result -= pow(degrees[com] / m, 2);
    }
    return result;
}

WeightMap neighcom(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    Nodes const &node2com,
    Node node)
{
    WeightMap neighbor_weight;
    Nodes neighbors = graph_neighbors[node];
    Weights neighbors_weight = graph_weights[node];

    for (size_t i = 0; i < neighbors.size(); i++)
    {
        Node neighbor = neighbors[i];
        if (neighbor == node)
            continue;

        Node neighborcom = node2com[neighbor];
        neighbor_weight[neighborcom] += neighbors_weight[i];
    }
    return neighbor_weight;
}

void one_level(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    Nodes &node2com,
    Weights &internals,
    Weights const &loops,
    Weights &degrees,
    Weights const &gdegrees,
    float total_weight,
    float resolution)
{
    bool modified = true;
    float cur_mod = modularity(internals,
                               degrees,
                               total_weight,
                               resolution);
    float new_mod = cur_mod;
    size_t n_nodes = graph_neighbors.size();
    float m = 2 * total_weight;
    while (modified)
    {
        modified = false;
        cur_mod = new_mod;

        for (Node node = 0; node < n_nodes; node++)
        {
            Node node_com = node2com[node];
            WeightMap neighbor_weight = neighcom(
                graph_neighbors, graph_weights, node2com, node);

            // remove
            Weight node_gdegree = gdegrees[node];
            Weight node_loop = loops[node];
            node2com[node] = -1;
            degrees[node_com] -= node_gdegree;
            internals[node_com] -= neighbor_weight[node_com] + node_loop;

            Node best_com = node_com;
            float best_increase = 0;
            for (auto [com, weight] : neighbor_weight)
            {
                if (weight <= 0)
                    continue;

                float increase = resolution * weight;
                increase -= degrees[com] * node_gdegree / m;

                if (increase > best_increase)
                {
                    best_increase = increase;
                    best_com = com;
                }
            }

            // insert
            node2com[node] = best_com;
            degrees[best_com] += node_gdegree;
            internals[best_com] += neighbor_weight[best_com] + node_loop;
            if (best_com != node_com)
                modified = true;
        }

        new_mod = modularity(internals,
                             degrees,
                             total_weight,
                             resolution);
        if (new_mod - cur_mod < 0.0000001)
            break;
    }
}

void one_level_prune(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    Nodes &node2com,
    Weights &internals,
    Weights const &loops,
    Weights &degrees,
    Weights const &gdegrees,
    float total_weight,
    float resolution)
{
    size_t n_nodes = graph_neighbors.size();
    float m = 2 * total_weight;

    NodeSet P;
    for (Node i = 0; i < n_nodes; i++)
    {
        P.insert(i);
    }

    while (P.size() != 0)
    {
        Node node = *P.begin();
        P.erase(P.begin());

        Node node_com = node2com[node];
        WeightMap neighbor_weight = neighcom(
            graph_neighbors, graph_weights, node2com, node);

        // remove
        node2com[node] = -1;
        degrees[node_com] -= gdegrees[node];
        internals[node_com] -= neighbor_weight[node_com] + loops[node];

        Node best_com = node_com;
        float best_increase = 0;
        for (auto [com, weight] : neighbor_weight)
        {
            if (weight <= 0)
                continue;

            float increase = resolution * weight;
            increase -= degrees[com] * gdegrees[node] / m;

            if (increase > best_increase)
            {
                best_increase = increase;
                best_com = com;
            }
        }

        // insert
        node2com[node] = best_com;
        degrees[best_com] += gdegrees[node];
        internals[best_com] += neighbor_weight[best_com] + loops[node];

        if (best_com != node_com)
        {
            Nodes neighbors = graph_neighbors[node];
            for (Node neighbor : neighbors)
            {
                if (neighbor == node)
                    continue;
                Node neighbor_c = node2com[neighbor];
                if (neighbor_c != best_com)
                    P.insert(neighbor);
            }
        }
    }
}

void one_step(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    Nodes &node2com,
    Weights &internals,
    Weights const &loops,
    Weights &degrees,
    Weights const &gdegrees,
    float total_weight,
    float resolution)
{
    size_t n_nodes = graph_neighbors.size();
    float m = 2 * total_weight;

    Node best_move_node;
    Node best_move_com;
    Node old_move_com;
    WeightMap best_neighbor_weight;

    float best_increase = -INFINITY;
    bool modified = false;
    for (Node node = 0; node < n_nodes; node++)
    {
        Node node_com = node2com[node];
        WeightMap neighbor_weight = neighcom(
            graph_neighbors, graph_weights, node2com, node);

        // remove
        Weight node_gdegree = gdegrees[node];
        Weight node_loop = loops[node];
        Weight com_weight = neighbor_weight[node_com];

        node2com[node] = -1;
        degrees[node_com] -= node_gdegree;
        internals[node_com] -= com_weight + node_loop;

        Node best_com = node_com;
        for (auto [com, weight] : neighbor_weight)
        {
            if (weight <= 0)
                continue;

            float increase = resolution * weight;
            increase -= degrees[com] * node_gdegree / m;
            if (increase > best_increase)
            {
                best_increase = increase;
                best_move_node = node;
                best_move_com = com;
                best_neighbor_weight = neighbor_weight;
                old_move_com = node_com;
                modified = true;
            }
        }

        // insert
        node2com[node] = node_com;
        degrees[node_com] += node_gdegree;
        internals[node_com] += com_weight + node_loop;
    }
    if (!modified)
        return;

    // remove
    node2com[best_move_node] = -1;
    degrees[old_move_com] -= gdegrees[best_move_node];
    internals[old_move_com] -= best_neighbor_weight[old_move_com] + loops[best_move_node];

    // insert
    node2com[best_move_node] = best_move_com;
    degrees[best_move_com] += gdegrees[best_move_node];
    internals[best_move_com] += best_neighbor_weight[best_move_com] + loops[best_move_node];
}

std::tuple<GraphNeighbors, Nodes> renumber(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    Nodes const &node2com)
{
    size_t n_nodes = node2com.size();
    Nodes com_n_nodes;
    com_n_nodes.resize(n_nodes);
    for (Node node = 0; node < n_nodes; node++)
        com_n_nodes[node2com[node]] += 1;

    Nodes com_new_index;
    com_new_index.resize(n_nodes);
    size_t final_index = 0;
    for (Node com = 0; com < n_nodes; com++)
    {
        if (com_n_nodes[com] <= 0)
            continue;

        com_new_index[com] = final_index;
        final_index++;
    }

    GraphNeighbors new_communities;
    new_communities.resize(final_index);
    Nodes new_node2com;
    new_node2com.resize(n_nodes);
    for (Node node = 0; node < n_nodes; node++)
    {
        Node com = node2com[node];
        Node new_com = com_new_index[com];
        new_communities[new_com].push_back(node);
        new_node2com[node] = new_com;
    }
    return std::make_tuple(new_communities, new_node2com);
}

std::tuple<GraphNeighbors, GraphWeights, size_t> induced_graph(
    GraphNeighbors const &graph_neighbors,
    GraphWeights const &graph_weights,
    GraphNeighbors const &communities,
    Nodes const &node2com)
{
    size_t new_n_nodes = communities.size();
    GraphNeighbors new_graph_neighbors;
    GraphWeights new_graph_weights;
    new_graph_neighbors.resize(new_n_nodes);
    new_graph_weights.resize(new_n_nodes);

    WeightMap to_insert;

    for (Node i = 0; i < new_n_nodes; i++)
    {
        to_insert.clear();
        Nodes nodes = communities[i];
        for (Node j = 0; j < nodes.size(); j++)
        {
            Node node = nodes[j];
            Nodes neighbors = graph_neighbors[node];
            Weights neighbors_weight = graph_weights[node];
            for (size_t k = 0; k < neighbors.size(); k++)
            {
                Node neighbor = neighbors[k];
                Weight neighbor_weight = neighbors_weight[k];
                Node neighbor_com = node2com[neighbor];
                if (neighbor == node)
                    to_insert[neighbor_com] += 2 * neighbor_weight;
                else
                    to_insert[neighbor_com] += neighbor_weight;
            }
        }
        for (auto [com_, weight_] : to_insert)
        {
            new_graph_neighbors[i].push_back(com_);
            if (com_ == i)
                new_graph_weights[i].push_back(weight_ / 2);
            else
                new_graph_weights[i].push_back(weight_);
        }
    }
    return std::make_tuple(
        new_graph_neighbors, new_graph_weights, new_n_nodes);
}

Nodes get_partition(Nodes const &node2com, size_t n_nodes)
{
    Nodes partition;
    for (size_t i = 0; i < n_nodes; i++)
    {
        partition.push_back(node2com[i]);
    }
    return partition;
}

std::vector<std::pair<Nodes, float>> generate_dendrogram(
    GraphNeighbors &graph_neighbors,
    GraphWeights &graph_weights,
    float resolution,
    bool prune,
    bool full)
{
    float mod;
    float new_mod;

    std::vector<std::pair<Nodes, float>> partition_list;
    GraphNeighbors communities;
    size_t n_nodes = graph_neighbors.size();

    // init_status
    auto [node2com,
          internals,
          loops,
          degrees,
          gdegrees,
          total_weight] = init_status(graph_neighbors, graph_weights);

    // one_level
    if (!prune)
        one_level(graph_neighbors, graph_weights,
                  node2com, internals, loops, degrees, gdegrees,
                  total_weight, resolution);
    else
        one_level_prune(graph_neighbors, graph_weights,
                        node2com, internals, loops, degrees, gdegrees,
                        total_weight, resolution);

    // new_mod
    new_mod = modularity(
        internals, degrees, total_weight, resolution);

    // renumber
    std::tie(communities, node2com) = renumber(
        graph_neighbors, graph_weights, node2com);

    // partition_list
    partition_list.push_back(
        std::make_pair(get_partition(node2com, n_nodes), new_mod));

    mod = new_mod;
    // induced graph
    std::tie(graph_neighbors, graph_weights, n_nodes) = induced_graph(
        graph_neighbors, graph_weights, communities, node2com);

    // init_status
    std::tie(node2com,
             internals,
             loops,
             degrees,
             gdegrees,
             total_weight) = init_status(graph_neighbors, graph_weights);

    while (true)
    {
        if (!prune)
            one_level(graph_neighbors, graph_weights,
                      node2com, internals, loops, degrees, gdegrees,
                      total_weight, resolution);
        else
            one_level_prune(graph_neighbors, graph_weights,
                            node2com, internals, loops, degrees, gdegrees,
                            total_weight, resolution);

        new_mod = modularity(
            internals, degrees, total_weight, resolution);

        if (new_mod - mod < 0.0000001)
            break;

        std::tie(communities, node2com) = renumber(
            graph_neighbors, graph_weights, node2com);
        mod = new_mod;
        partition_list.push_back(
            std::make_pair(get_partition(node2com, n_nodes), new_mod));

        std::tie(graph_neighbors, graph_weights, n_nodes) = induced_graph(
            graph_neighbors, graph_weights, communities, node2com);

        std::tie(node2com,
                 internals,
                 loops,
                 degrees,
                 gdegrees,
                 total_weight) = init_status(graph_neighbors, graph_weights);
    }

    if (full)
    {
        size_t node2com_size = node2com.size();
        while (true)
        {
            // one iteration
            one_step(graph_neighbors, graph_weights,
                     node2com, internals, loops, degrees, gdegrees,
                     total_weight, resolution);
            new_mod = modularity(
                internals, degrees, total_weight, resolution);
            std::tie(communities, node2com) = renumber(
                graph_neighbors, graph_weights, node2com);
            partition_list.push_back(
                std::make_pair(get_partition(node2com, n_nodes), new_mod));
            std::tie(graph_neighbors, graph_weights, n_nodes) = induced_graph(
                graph_neighbors, graph_weights, communities, node2com);
            std::tie(node2com,
                     internals,
                     loops,
                     degrees,
                     gdegrees,
                     total_weight) = init_status(graph_neighbors, graph_weights);
            if (node2com.size() == node2com_size || node2com.size() == 1)
                break;

            node2com_size = node2com.size();
        }
    }
    return partition_list;
}
