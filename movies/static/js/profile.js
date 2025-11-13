
document.addEventListener("DOMContentLoaded", () => {
    const follow = document.querySelectorAll(".follow-btn");

    if (follow.length > 0) {
        const requestProfile = follow[0].attributes.requestProfile.value;
        const profileUser = follow[0].attributes.Profile.value;
        fetch('/profile_data/')
            .then(response => response.json())
            .then(data => {
                const followers = data.followers;
                const res = followers.includes(profileUser);
                if (res) {
                    follow[0].textContent = "Unfollow";
                }
            });
    }

    


    document.addEventListener("click", (event) => {
        if (event.target.classList.contains("follow-btn")) {
            const requestProfile = follow[0].attributes.requestProfile.value;
            const profileUser = follow[0].attributes.Profile.value;

            if (follow[0].textContent === "Follow") {
                console.log("Follow button clicked");
                fetch(`/followRequest/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"), // 🔒 Required for Django
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        requestProfile: requestProfile,
                        profileUser: profileUser,
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.status === "success") {
                            follow[0].textContent = "Unfollow";
                        }
                    })
                    .catch(error => console.error("Error:", error));
            }
            else {
                fetch(`/UnfollowRequest/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"), // 🔒 Required for Django
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        requestProfile: requestProfile,
                        profileUser: profileUser,
                    })
                })
                .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.status === "success") {
                            follow[0].textContent = "Follow";
                        }
                    })
                    .catch(error => console.error("Error:", error));
            }
        }
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

