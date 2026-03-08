from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Player data now includes official 2025 IPL headshot URLs.
players = [
   {"id":1,"name":"Virat Kohli","team":"RCB","nationality":"India","base_price":2000000,"winning_bid":2000000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/2.png"},
    {"id":2,"name":"Rohit Sharma","team":"MI","nationality":"India","base_price":2000000,"winning_bid":2000000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/6.png"},
    {"id":3,"name":"MS Dhoni","team":"CSK","nationality":"India","base_price":2000000,"winning_bid":2000000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/57.png"},
    {"id":4,"name":"KL Rahul","team":"LSG","nationality":"India","base_price":1800000,"winning_bid":1800000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/19.png"},
    {"id":5,"name":"Hardik Pandya","team":"MI","nationality":"India","base_price":1800000,"winning_bid":1800000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/54.png"},
    {"id":6,"name":"Rishabh Pant","team":"DC","nationality":"India","base_price":1700000,"winning_bid":1700000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/18.png"},
    {"id":7,"name":"Shubman Gill","team":"GT","nationality":"India","base_price":1600000,"winning_bid":1600000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/62.png"},
    {"id":8,"name":"Jasprit Bumrah","team":"MI","nationality":"India","base_price":1700000,"winning_bid":1700000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/9.png"},
    {"id":9,"name":"Ravindra Jadeja","team":"CSK","nationality":"India","base_price":1600000,"winning_bid":1600000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2024/46.png"},
    {"id":10,"name":"Surya Kumar Yadav","team":"MI","nationality":"India","base_price":1600000,"winning_bid":1600000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/174.png"},
    {"id":11,"name":"Sanju Samson","team":"RR","nationality":"India","base_price":1500000,"winning_bid":1500000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2024/190.png"},
    {"id":12,"name":"Yuzvendra Chahal","team":"RR","nationality":"India","base_price":1400000,"winning_bid":1400000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/10.png"},
    {"id":13,"name":"Shreyas Iyer","team":"KKR","nationality":"India","base_price":1500000,"winning_bid":1500000,"capped_status":"Capped", "image": "https://www.punjabkingsipl.in/static-assets/images/players/63961.png?v=6.34"},
    {"id":14,"name":"Ishan Kishan","team":"MI","nationality":"India","base_price":1400000,"winning_bid":1400000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/164.png"},
    {"id":15,"name":"Axar Patel","team":"DC","nationality":"India","base_price":1300000,"winning_bid":1300000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/110.png"},
    {"id":16,"name":"Ruturaj Gaikwad","team":"CSK","nationality":"India","base_price":1400000,"winning_bid":1400000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/102.png"},
    {"id":17,"name":"Tilak Varma","team":"MI","nationality":"India","base_price":1200000,"winning_bid":1200000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/993.png"},
    {"id":18,"name":"Arshdeep Singh","team":"PBKS","nationality":"India","base_price":1100000,"winning_bid":1100000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/125.png"},
    {"id":19,"name":"Mohammed Siraj","team":"RCB","nationality":"India","base_price":1200000,"winning_bid":1200000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/63.png"},
    {"id":20,"name":"Kuldeep Yadav","team":"DC","nationality":"India","base_price":1100000,"winning_bid":1100000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/14.png"},
    {"id":21,"name":"Rinku Singh","team":"KKR","nationality":"India","base_price":800000,"winning_bid":800000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/152.png" },
    {"id":22,"name":"Abhishek Sharma","team":"SRH","nationality":"India","base_price":800000,"winning_bid":800000,"capped_status":"Capped", "image": "https://static.toiimg.com/photo/119127542.cms"},
    {"id":23,"name":"Rahul Tewatia","team":"GT","nationality":"India","base_price":800000,"winning_bid":800000,"capped_status":"Capped", "image": "https://static.toiimg.com/photo/120687125.cms"},
    {"id":24,"name":"Venkatesh Iyer","team":"KKR","nationality":"India","base_price":900000,"winning_bid":900000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/584.png"},
    {"id":25,"name":"Devdutt Padikkal","team":"RCB","nationality":"India","base_price":900000,"winning_bid":900000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/200.png"},
    {"id":26,"name":"Shivam Dube","team":"CSK","nationality":"India","base_price":900000,"winning_bid":900000,"capped_status":"Capped", "image": "https://www.iplbetonline.in/wp-content/uploads/2023/04/211.png"},
    {"id":27,"name":"T Natarajan","team":"SRH","nationality":"India","base_price":800000,"winning_bid":800000,"capped_status":"Capped", "image": "https://www.iplbetonline.in/wp-content/uploads/2023/04/3831.png"},
    {"id":28,"name":"Krunal Pandya","team":"RCB","nationality":"India","base_price":900000,"winning_bid":900000,"capped_status":"Capped", "image": "https://documents.iplt20.com/ipl/IPLHeadshot2025/1483.png"},
    {"id":29,"name":"Shashank Singh","team":"PBKS","nationality":"India","base_price":1000000,"winning_bid":1000000,"capped_status":"Capped", "image":"https://documents.iplt20.com/ipl/IPLHeadshot2025/191.png"},
    {"id":30,"name":"Varun Chakravarthy","team":"KKR","nationality":"India","base_price":900000,"winning_bid":900000,"capped_status":"Capped", "image": "https://static.toiimg.com/photo/119129071.cms"}



]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/players")
def get_players():
    return jsonify(players)

@app.route("/bid", methods=["POST"])
def place_bid():
    data = request.get_json()
    player_id = int(data["player_id"])
    amount = int(data["amount"])

    for player in players:
        if player["id"] == player_id:
            current_price = max(player.get("winning_bid", 0), player.get("base_price", 0))

            if amount <= current_price:
                error_message = f"Bid must be higher than the current price of ₹{current_price}"
                return jsonify({"error": error_message}), 400

            player["winning_bid"] = amount
            return jsonify({"success": True, "player": player})

    return jsonify({"error": "Player not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)