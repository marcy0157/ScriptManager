import instaloader
import os


def save_results_to_file(base_name, results):
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    count = 0
    while True:
        filename = f"{base_name}{count}.txt" if count > 0 else f"{base_name}.txt"
        filepath = os.path.join(results_dir, filename)
        if not os.path.exists(filepath):
            break
        count += 1

    try:
        with open(filepath, 'w') as f:
            for result in results:
                f.write(result + '\n')
        print(f"Results saved in {filepath}")
    except Exception as e:
        print(f"Error writing file: {e}")


def osintgram_instagram_scraper():
    print("OSINTgram - Instagram Data Collection Tool")
    username = input("Enter the target Instagram username: ")

    L = instaloader.Instaloader()

    results = []

    try:
        # Carica il profilo Instagram
        profile = instaloader.Profile.from_username(L.context, username)

        # Raccoglie informazioni di base
        result_str = f"Profile: {profile.username}\n"
        result_str += f"Full Name: {profile.full_name}\n"
        result_str += f"Followers: {profile.followers}\n"
        result_str += f"Following: {profile.followees}\n"
        result_str += f"Bio: {profile.biography}\n"
        result_str += f"External URL: {profile.external_url}\n"
        result_str += f"Number of Posts: {profile.mediacount}\n"
        results.append(result_str)
        print(result_str)

        # Raccoglie informazioni sui post
        posts = profile.get_posts()
        for post in posts:
            post_info = f"Post URL: https://www.instagram.com/p/{post.shortcode}/\n"
            post_info += f"Date: {post.date_utc}\n"
            post_info += f"Likes: {post.likes}\n"
            post_info += f"Comments: {post.comments}\n"
            post_info += f"Caption: {post.caption}\n"
            print(post_info)
            results.append(post_info)

        # Salva i risultati
        save_results_to_file(f"osintgram_{username}_results", results)

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: The profile '{username}' does not exist.")
    except Exception as e:
        print(f"Error: {e}")


osintgram_instagram_scraper()
