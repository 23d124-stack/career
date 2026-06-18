import requests

APP_ID = "c40602e2"
APP_KEY = "d3eaec5531e603cdaf4b03304dcae214"

def get_jobs(role):

    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what={role}"
    )

    response = requests.get(url)
    data = response.json()

    jobs = []

    for job in data.get("results", []):

        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),

            # 🔥 FIX HERE
            "apply_link": job.get("redirect_url")
        })

    return jobs