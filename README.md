<h1>Adcore Payments Application</h1>

<p>This is a full-stack application built with Angular (frontend) and FastAPI (backend). It supports managing payments and provides features like adding, viewing, and sorting payment entries.</p>

<hr />

<h2>Features</h2>
<ul>
  <li><strong>Frontend:</strong> Built with Angular</li>
  <li><strong>Backend:</strong> Powered by FastAPI</li>
  <li><strong>Database:</strong> MongoDB for data storage</li>
  <li><strong>Hosting:</strong> Frontend hosted on Netlify, backend hosted on Render</li>
  <li><strong>Functionality:</strong> RESTful APIs for payment management with features like adding, viewing, and sorting payment entries</li>
</ul>

<hr />

<h2>Steps to Run the Application Locally</h2>

<h3>Prerequisites</h3>
<ol>
  <li>Install <a href="https://nodejs.org/">Node.js</a> (version 18 or higher).</li>
  <li>Install <a href="https://www.python.org/">Python</a> (version 3.10 or higher).</li>
  <li>Install <a href="https://angular.io/cli">Angular CLI</a>.</li>
  <li>Have access to a MongoDB instance (local or Atlas).</li>
</ol>

<hr />

<h3>Clone the Repository</h3>
<pre>
<code>
git clone https://github.com/sahil3471/AdcoreClean.git
cd AdcoreClean
</code>
</pre>

<hr />

<h3>Backend Setup</h3>
<ol>
  <li>Navigate to the <code>backend</code> folder:
    <pre><code>cd backend</code></pre>
  </li>
  <li>Create a virtual environment:
    <pre>
<code>
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
</code>
    </pre>
  </li>
  <li>Install the required Python packages:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Create a <code>.env</code> file with the following content:
    <pre>
<code>
MONGO_URI=mongodb+srv://&lt;username&gt;:&lt;password&gt;@cluster0.mongodb.net/dbname
</code>
    </pre>
    Replace <code>&lt;username&gt;</code>, <code>&lt;password&gt;</code>, and <code>dbname</code> with your MongoDB credentials.
  </li>
  <li>Run the backend server:
    <pre><code>uvicorn main:app --reload</code></pre>
  </li>
  <li>Test the backend API:
    <ul>
      <li>Visit <a href="http://127.0.0.1:8000/test-connection">http://127.0.0.1:8000/test-connection</a>.</li>
    </ul>
  </li>
</ol>

<hr />

<h3>Frontend Setup</h3>
<ol>
  <li>Navigate to the <code>frontend/adcore-payments-ui</code> folder:
    <pre><code>cd ../frontend/adcore-payments-ui</code></pre>
  </li>
  <li>Install Node.js dependencies:
    <pre><code>npm install</code></pre>
  </li>
  <li>Update the environment file:
    <ul>
      <li>Open <code>src/environments/environment.ts</code> and update the backend API URL:
        <pre>
<code>
export const environment = {
  production: false,
  apiBaseUrl: 'http://127.0.0.1:8000', // Use the Render URL for production
};
</code>
        </pre>
      </li>
    </ul>
  </li>
  <li>Run the frontend development server:
    <pre><code>ng serve</code></pre>
  </li>
  <li>Open the application in your browser:
    <ul>
      <li>Visit <a href="http://localhost:4200">http://localhost:4200</a>.</li>
    </ul>
  </li>
</ol>

<hr />

<h2>Environment Variables</h2>

<h3>Backend</h3>
<ul>
  <li><code>MONGO_URI</code>: MongoDB connection string (e.g., <code>mongodb+srv://&lt;username&gt;:&lt;password&gt;@cluster0.mongodb.net/dbname</code>).</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li><code>apiBaseUrl</code>: URL of the backend API (e.g., <code>http://127.0.0.1:8000</code> for local or Render URL for production).</li>
</ul>

<hr />

<h2>Live Deployment</h2>

<h3>Frontend</h3>
<ul>
  <li>Hosted on Netlify: <a href="https://adcorefullstack.netlify.app">Frontend Live URL</a></li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Hosted on Render: <a href="https://adcorefullstack.onrender.com">Backend Live URL</a></li>
</ul>

<hr />

<h2>Built With</h2>
<ul>
  <li>Angular</li>
  <li>FastAPI</li>
  <li>MongoDB</li>
  <li>Netlify</li>
  <li>Render</li>
</ul>

<hr />

<h2>Contributing</h2>
<ol>
  <li>Fork the repository.</li>
  <li>Create a new branch:
    <pre><code>git checkout -b feature/your-feature-name</code></pre>
  </li>
  <li>Make your changes and commit them:
    <pre><code>git commit -m "Add your feature"</code></pre>
  </li>
  <li>Push your changes:
    <pre><code>git push origin feature/your-feature-name</code></pre>
  </li>
  <li>Open a pull request.</li>
</ol>

<hr />

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>
