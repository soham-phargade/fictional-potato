import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple
import json

@dataclass
class Paper:
    """Represents a research paper node"""
    title: str
    authors: List[str]
    link: str = ""
    doi: str = ""
    published_link: str = ""
    venue: str = ""
    
    def __hash__(self):
        return hash(self.title)
    
    def __eq__(self, other):
        return isinstance(other, Paper) and self.title == other.title

@dataclass
class Edge:
    """Represents a connection between two papers"""
    paper1: str  # title of first paper
    paper2: str  # title of second paper
    weight: float
    connection_type: str  # 'author', 'citation', 'topic'
    shared_elements: List[str] = field(default_factory=list)

class PublicationGraph:
    """Graph representation of publications"""
    
    def __init__(self):
        self.papers: Dict[str, Paper] = {}
        self.edges: List[Edge] = []
        self.author_index: Dict[str, Set[str]] = defaultdict(set)  # author -> paper titles
    
    def add_paper(self, paper: Paper):
        """Add a paper node to the graph"""
        self.papers[paper.title] = paper
        for author in paper.authors:
            self.author_index[author].add(paper.title)
    
    def build_edges(self, author_weight=1.0, min_shared_authors=1):
        """Build edges based on shared authors"""
        self.edges = []
        
        # Create edges for papers with shared authors
        processed_pairs = set()
        
        for author, paper_titles in self.author_index.items():
            paper_list = list(paper_titles)
            for i in range(len(paper_list)):
                for j in range(i + 1, len(paper_list)):
                    pair = tuple(sorted([paper_list[i], paper_list[j]]))
                    if pair not in processed_pairs:
                        processed_pairs.add(pair)
                        
                        # Find all shared authors
                        p1 = self.papers[paper_list[i]]
                        p2 = self.papers[paper_list[j]]
                        shared = set(p1.authors) & set(p2.authors)
                        
                        if len(shared) >= min_shared_authors:
                            weight = len(shared) * author_weight
                            edge = Edge(
                                paper1=paper_list[i],
                                paper2=paper_list[j],
                                weight=weight,
                                connection_type='author',
                                shared_elements=list(shared)
                            )
                            self.edges.append(edge)
    
    def get_statistics(self):
        """Get graph statistics"""
        return {
            'num_papers': len(self.papers),
            'num_edges': len(self.edges),
            'num_authors': len(self.author_index),
            'avg_authors_per_paper': sum(len(p.authors) for p in self.papers.values()) / len(self.papers) if self.papers else 0,
            'avg_papers_per_author': sum(len(papers) for papers in self.author_index.values()) / len(self.author_index) if self.author_index else 0
        }
    
    def get_paper_connections(self, title: str) -> List[Edge]:
        """Get all edges connected to a specific paper"""
        return [e for e in self.edges if e.paper1 == title or e.paper2 == title]
    
    def to_dict(self):
        """Export graph as dictionary for JSON serialization"""
        return {
            'nodes': [
                {
                    'id': title,
                    'title': paper.title,
                    'authors': paper.authors,
                    'link': paper.link,
                    'doi': paper.doi,
                    'published_link': paper.published_link,
                    'venue': paper.venue
                }
                for title, paper in self.papers.items()
            ],
            'edges': [
                {
                    'source': edge.paper1,
                    'target': edge.paper2,
                    'weight': edge.weight,
                    'type': edge.connection_type,
                    'shared': edge.shared_elements
                }
                for edge in self.edges
            ],
            'statistics': self.get_statistics()
        }


class PublicationParser:
    """Parser for PARASOL LAB publication format"""
    
    @staticmethod
    def normalize_author(author: str) -> str:
        """Normalize author name for matching"""
        # Remove extra whitespace and standardize format
        author = author.strip()
        # Remove common suffixes
        author = re.sub(r',?\s*(Jr\.?|Sr\.?|III?|IV)$', '', author)
        return author
    
    @staticmethod
    def parse_authors(author_string: str) -> List[str]:
        """Parse comma-separated authors"""
        # Remove trailing commas and split
        authors = [a.strip() for a in author_string.rstrip(',').split(',')]
        # Filter out empty strings and normalize
        authors = [PublicationParser.normalize_author(a) for a in authors if a.strip()]
        # Filter out venue information (typically contains years or special keywords)
        authors = [a for a in authors if not re.search(r'\d{4}|Proceedings|Workshop|Conference|ArXiv', a)]
        return authors
    
    @staticmethod
    def parse_file(content: str) -> PublicationGraph:
        """Parse the publication file and create graph"""
        graph = PublicationGraph()
        
        # Split by paper separator
        papers_raw = content.split('---')
        
        for paper_text in papers_raw:
            paper_text = paper_text.strip()
            if not paper_text or '===' in paper_text:
                continue
            
            # Extract fields
            title_match = re.search(r'TITLE:\s*(.+?)(?=\n|$)', paper_text)
            authors_match = re.search(r'AUTHORS:\s*(.+?)(?=\n|$)', paper_text, re.DOTALL)
            link_match = re.search(r'LINK:\s*(.+?)(?=\n|$)', paper_text)
            doi_match = re.search(r'DOI:\s*(.+?)(?=\n|$)', paper_text)
            pub_link_match = re.search(r'PUBLISHED LINK:\s*(.+?)(?=\n|$)', paper_text)
            
            if not title_match or not authors_match:
                continue
            
            title = title_match.group(1).strip()
            authors_raw = authors_match.group(1).strip()
            authors = PublicationParser.parse_authors(authors_raw)
            
            paper = Paper(
                title=title,
                authors=authors,
                link=link_match.group(1).strip() if link_match else "",
                doi=doi_match.group(1).strip() if doi_match else "",
                published_link=pub_link_match.group(1).strip() if pub_link_match else ""
            )
            
            graph.add_paper(paper)
        
        # Build edges after all papers are added
        graph.build_edges()
        
        return graph


# Example usage
if __name__ == "__main__":
#     sample_input = """=== PARASOL LAB PUBLICATIONS ===

# TITLE: K-ARC: Adaptive Robot Coordination for Multi-Robot Kinodynamic Planning
# AUTHORS: Mike Qin, Irving Solis, James Motes, Marco Morales, Nancy M. Amato, ArXiv,
# LINK: https://www.arxiv.org/abs/2501.01559
# DOI: https://doi.org/10.48550/arXiv.2501.01559
# ---

# TITLE: A primer on in vitro biological neural networks
# AUTHORS: Frithjof Gressmann, Ashley Chen, Lily Hexuan Xie, Sarah Dowden, Nancy Amato, Lawrence Rauchwerger, NeurIPS 2024 Workshop Machine Learning with new Compute Paradigms, Vancouver, Canada,
# PUBLISHED LINK: https://openreview.net/forum?id=RdFI2ogt1j
# """
    with open("publication_data.txt", "r") as f:
        sample_input = f.read()

    # Parse and build graph
    parser = PublicationParser()
    graph = parser.parse_file(sample_input)

    with open("graph.json", "w") as f:
        json.dump(graph.to_dict(), f, indent=2)
    print("Graph exported to graph.json")
    
    # Display statistics
    stats = graph.get_statistics()
    print("Graph Statistics:")
    print(f"  Papers: {stats['num_papers']}")
    print(f"  Edges: {stats['num_edges']}")
    print(f"  Authors: {stats['num_authors']}")
    print(f"  Avg authors per paper: {stats['avg_authors_per_paper']:.2f}")
    print(f"  Avg papers per author: {stats['avg_papers_per_author']:.2f}")
    
    # Display papers
    print("\nPapers:")
    for title, paper in graph.papers.items():
        print(f"  - {title}")
        print(f"    Authors: {', '.join(paper.authors)}")
    
    # Display edges
    print("\nConnections:")
    for edge in graph.edges:
        print(f"  {edge.paper1[:50]}... <-> {edge.paper2[:50]}...")
        print(f"    Shared authors: {', '.join(edge.shared_elements)}")
        print(f"    Weight: {edge.weight}")