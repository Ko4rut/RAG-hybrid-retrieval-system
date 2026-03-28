from langchain_community.document_loaders import DirectoryLoader,UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


loader = DirectoryLoader(
    path="./Corpus",
    glob= "**/*.pdf",
    loader_cls=UnstructuredFileLoader,
    show_progress= True,
    use_multithreading= True

)

MARKDOWN_SEPERATORS = [
    "\n#{1,6}",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",

]

docs = loader.load()

 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1200,
    chunk_overlap = 200,
    add_start_index = True,
    strip_whitespace = True,
    separators= MARKDOWN_SEPERATORS,
)

from pprint import pprint

splits =text_splitter.split_documents(docs)
pprint(splits)