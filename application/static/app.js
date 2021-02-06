//Searches for books based on title and loads them to the screen.
async function search_book(searchterm){
    url = 'https://www.googleapis.com/books/v1/volumes?q=';
    resp = await axios.get(`${url}${searchterm}`);
    data = resp.data.items;
    username = $("#user").text();
    res = await axios.get(`/users/search/${username}`);
    $user = res.data;
    $row = $("#top_book_row");
    $row.empty();
    for(let point in data){
        img = data[point]['volumeInfo']['imageLinks']['thumbnail'];
        title = data[point]['volumeInfo']['title'];
        book_card = `<div class="card col-2 my-1 mx-auto">
                        <img src="${img}" 
                            alt="${title}" 
                            class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">${title}</h5>
                            <a href="/users/${$user}/library/check/${title}" class="btn btn-success my-1">Add to Library</a>
                            <a href="/books/check/${title}" class="btn btn-primary my-1">View Details</a>
                        </div>
                    </div>`;
        $row.append(book_card);
    }
}
//validates book that a user is starting a book club on.
async function validate_book(book_title){
    $book_val = $("#book_val");
    url = 'https://www.googleapis.com/books/v1/volumes?q=';
    resp = await axios.get(`${url}${book_title}`);
    data = resp.data.items;
    username = $("#user").text();
    res = await axios.get(`/users/search/${username}`);
    $user = res.data;
    $book_val.empty();
    for(let point in data){
        title = data[point]['volumeInfo']['title'];
        author = data[point]['volumeInfo']['authors'];
        image = data[point]['volumeInfo']['imageLinks']['thumbnail'];
        book_selector = `
            <div class="col-2 my-2">
                <div class="row">
                    <img src="${image}" alt="${title} />
                </div>
                <div class="row">
                    <label for="${title}_radio" class="form-check-label text-center">${title}</label>
                </div>
                <div class="row text-center">
                    <h6>${author}</h6>
                </div>
            </div>`;
        $book_val.append(book_selector);
    }
}
function open_comment(e){
    e.preventDefault();
    $form = $("#comment-form")
    $("#reply").addClass("disabled");
    $form.removeClass("invisible");
}

function book_search(e){
    e.preventDefault();
    $search_term = $("#search_bar").val();
    search_book($search_term);
}

function book_validate(e){
    e.preventDefault();
    $("#validate").remove();
    $("#message").append("<h4>Please select the correct book below.</h4>")
    $book = $("#book").val();
    validate_book($book);
}

$('#search').on("click", book_search);
$("#validate").on("click", book_validate);
$("#reply").on("click", open_comment);
