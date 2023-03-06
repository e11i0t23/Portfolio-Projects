function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const username = JSON.parse(document.getElementById('user_name').textContent);
const auth = JSON.parse(document.getElementById('authenticated').textContent);
const approot = ReactDOM.createRoot(document.getElementById("app"))

var pfroot = undefined;
if (auth) {
    pfroot = ReactDOM.createRoot(document.querySelector("#PostForm"))
}


function PostForm() {

    const [state, setState] = React.useState({
        text: "",
        submit: false
    })

    function updateText(event) {
        setState({
            text: event.target.value,
            submit: event.target.value == "" ? false : true
        })
    }

    // Submit the Post to the server
    function submitPost() {
        fetch('/network/api/post/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                post: state.text
            })
        }).then(x => {
            setState({
                text: "",
                submit: false
            })
            approot.render(<Posts key={Math.random()} />);
        }
        )
    }
    return (
        <div>
            <div className="cont">
                <textarea type="text-area" value={state.text} onChange={updateText} cols={60} rows={4} />
                <br />
                <button className="btn btn-outline-primary" disabled={!state.submit} onClick={submitPost}>Post</button>
            </div>
        </div>
    )
}


function Posts(props) {
    const [state, setState] = React.useState({
        data: [],
        isLoading: true,
        pages: 1
    })
    const [page, setPage] = React.useState(0)

    // Fetch all our posts to render, and reload them when page changes
    React.useEffect(() => {
        fetch(props['user'] ? `/network/api/posts/${page}/user/${props['user']}` : props['following'] ? `/network/api/posts/${page}/following` : `/network/api/posts/${page}/`)
            .then(response => { return response.json() })
            .then(data => {
                setState({
                    ...state,
                    data: data.posts,
                    pages: data.pages,
                    isLoading: false
                })
            })
    }, [page])

    const changePage = (e) => {
        e.preventDefault()
        const p = e.target.dataset.page
        console.log("p", p)
        switch (p) {
            case "prv":
                if (page != 0) {
                    setPage(page - 1)
                }
                break;
            case "nxt":
                if (page != (state.pages - 1)) {
                    setPage(page + 1)
                }
                break;
            default:
                const pInt = parseInt(p)
                console.log("pint", pInt)
                if (page == pInt) return false
                setPage(pInt)
                break;
        }

    }

    if (state.isLoading) return (<div>Loading...</div>)
    return (
        <div>
            <div className='row'>
                {state.data.map(post => <Post key={post.id} post={post}></Post>)}
            </div>
            <nav aria-label="Page navigation">
                <ul className="pagination justify-content-center">
                    <li className={`page-item ${(page == 0 && `disabled`)}`}><a className="page-link" data-page="prv" onClick={changePage} href="">Previous</a></li>
                    {Array.apply(0, Array(state.pages)).map(function (x, i) {
                        return <li key={i} className={`page-item ${(page == i && `active`)}`}><a className="page-link" data-page={i} onClick={changePage} href="">{i + 1}</a></li>;
                    })}
                    <li className={`page-item ${(page == state.pages - 1 && `disabled`)}`}><a className="page-link" data-page="nxt" onClick={changePage} href="">Next</a></li>
                </ul>
            </nav>
        </div>
    )

}

function Post(props) {
    var post = props['post']
    const [state, setState] = React.useState({
        liked: post.liked,
        likes: post.likes,
        body: post.body,
        edit: false,
    })

    // Handle editing a post and submitting this to the server
    function edit() {
        // The same funciton is used for editing and subbmiting therefore we need to know which state were in
        if (!state.edit) {
            setState({ ...state, edit: true })
        } else {
            fetch(`/network/api/post/${post.id}`, {
                method: 'PUT',
                headers: { 'X-CSRFToken': csrftoken },
                body: JSON.stringify({
                    post: state.body
                })
            })
                .then(response => { return response.json() })
                .then(p => {
                    setState({
                        ...state,
                        edit: false,
                        body: p.body
                    })
                }
                )
        }
    }

    // simple function for updating the text area state value
    function updateText(event) {
        setState({
            ...state,
            body: event.target.value
        })
    }

    // Update the like status of a post on the server
    function like() {
        fetch(`/network/api/post/${post.id}`, {
            method: 'PUT',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                liked: !state.liked
            })
        })
            .then(response => { return response.json() })
            .then(p => {
                setState({
                    ...state,
                    liked: p.liked,
                    likes: p.likes
                })
            }
            )
    }

    return (
        <div className="col-12 col-md-6">
            <div className="post">
                <div className="row">
                    <div className="col-10">
                        <a className="usr-btn" data-userid={post.userid} onClick={userclick} href=""><h3>{post.user}</h3></a>
                    </div>
                    <div className="col-2 text-right">
                        {post.user == username
                            ? <button className="btn btn-outline-dark btn-sm editbtn" onClick={edit}>{state.edit ? 'submit' : 'Edit'}</button>
                            : (auth && <button className="btn btn-outline-danger btn-sm editbtn" onClick={like}>{state.liked ? 'UnLike' : 'Like'}</button>)
                        }
                    </div>
                </div>
                {state.edit
                    ? <textarea type="textarea" value={state.body} cols={60} rows={5} onChange={updateText} />
                    : <div>{state.body}</div>
                }
                <hr></hr>
                <p className="float-left">{post.timestamp}</p>
                <p className="float-right">Likes:{state.likes}</p>
            </div>
        </div>
    )
}

function User({ userid }) {
    let [isLoading, setIsLoading] = React.useState(true)
    let [state, setState] = React.useState({
        following: false,
        followerCount: 0,
        followingCount: 0
    })

    let username = React.useRef(null)

    // On load we fetch the users information
    React.useEffect(() => {
        fetch(`/network/api/user/${userid}`)
            .then(response => { return response.json() })
            .then(u => {
                setState({
                    following: u.following,
                    followerCount: u.followerCount,
                    followingCount: u.followingCount
                })
                username.current = u.username
                setIsLoading(false)
            }
            )

    }, [])

    // Update the following status of the user
    function follow() {
        fetch(`/network/api/user/${userid}`, {
            method: 'PUT',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                following: !state.following
            })
        })
            .then(response => { return response.json() })
            .then(u => {
                setState({
                    following: u.following,
                    followerCount: u.followerCount,
                    followingCount: u.followingCount
                })
                setIsLoading(false)
            })
    }


    if (isLoading) return (<div>Loading...</div>)
    return (
        <div>
            <div className="row">
                <div className="col-10">
                    <h2>{username.current}</h2>
                </div>
                <div className="col-1">
                    {(userid != user_id && auth) &&
                        <button className="btn btn-outline-primary btn-sm" onClick={follow}>{state.following ? 'Unfollow' : 'Follow'}</button>
                    }
                </div>
                <div className="col-1">
                    <div>Followers: {state.followerCount}</div>
                    <div>Following: {state.followingCount}</div>
                </div>
            </div>

            <Posts key={userid} user={userid} />
        </div>
    )
}




// Setup out button actions for title bar buttons
// In each case we show an appropriate set of posts and enable or disable the post form
ReactDOM.createRoot(document.getElementById("app")).render(<Posts />);

if (auth) pfroot.render(<PostForm />);

if (document.querySelector('#following-btn')) {
    document.querySelector('#following-btn').addEventListener('click', (e) => {
        e.preventDefault();
        console.log("followAuth:", auth)
        if (auth) pfroot.render(<PostForm key={0} />);
        approot.render(<Posts key="following" following={true} />)
    })
}

document.querySelectorAll('.index-btn').forEach(button => {
    button.onclick = (e) => {
        e.preventDefault();
        if (auth) pfroot.render(<PostForm key={1} />);
        approot.render(<Posts key="index" />);
    }
})

document.querySelectorAll('.usr-btn').forEach(button => {
    button.onclick = userclick
})

function userclick(e) {
    if (auth) pfroot.render(<div></div>)
    e.preventDefault();
    let userid = e.currentTarget.dataset.userid
    approot.render(<User key={userid} userid={userid} />);
    return false
}