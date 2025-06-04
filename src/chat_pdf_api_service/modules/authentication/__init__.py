from .route import authentication
from .model import User


"""_summary_
1. Add the user id and the unique doc id to each pdf document while inserting into the vector store
2. When trying to chat with a pdf a request is sent from the client whch would contain the userId and doc Id, which
the vector store would use to query
3. A user can also delete their document(from the vector store)
4. A scheduled job would be set-up to delete vector embediings in the vector store
that has stayed more than 24 hours to free up space
    """