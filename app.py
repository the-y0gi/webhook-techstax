from flask import Flask, request, jsonify, render_template
from database import save_webhook_data, fetch_latest_actions
from datetime import datetime, timezone 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/actions', methods=['GET'])
def get_actions():
    actions = fetch_latest_actions()
    return jsonify(actions)

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        event_type = request.headers.get('X-GitHub-Event')
        author = data.get('sender', {}).get('login', 'Unknown')
        

        timestamp = datetime.now(timezone.utc).strftime('%d %B %Y - %I:%M %p UTC')
        
        action_info = None

        if event_type == 'push':
            action_info = {
                "author": author,
                "request_id": data.get('after'), 
                "from_branch": None,
                "to_branch": data.get('ref', '').split('/')[-1],
                "timestamp": timestamp,
                "action": "PUSH" 
            }

        elif event_type == 'pull_request':
            pr_data = data.get('pull_request', {})
            is_merged = pr_data.get('merged', False) 
            
            action_info = {
                "author": author,
                "request_id": str(pr_data.get('number', pr_data.get('id'))), 
                "from_branch": pr_data.get('head', {}).get('ref'),
                "to_branch": pr_data.get('base', {}).get('ref'),
                "timestamp": timestamp,
                "action": "MERGE" if is_merged else "PULL_REQUEST" 
            }

        if action_info:
            save_webhook_data(action_info) 
            print(f"Successfully saved {event_type} event!")
            return jsonify({"status": "success"}), 200

        return jsonify({"status": "ignored event"}), 200

    except Exception as e:
        print(f"Error occurred: {e}") 
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)