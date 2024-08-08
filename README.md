<!DOCTYPE html>
<html lang="en">
<body>
<h1>SearchMaster</h1>

<p>SearchMaster is an advanced Google search tool designed for performing dork and normal scans. It allows users to retrieve and analyze search results based on customizable queries and filters.</p>

<h2>Features</h2>
<ul>
    <li><strong>Dork Scan</strong>: Search using predefined dork queries to find hidden or sensitive information.</li>
    <li><strong>Normal Scan</strong>: Perform a standard Google search based on user-provided terms.</li>
    <li><strong>Result Filtering</strong>: Filter results for social media links or specific file types.</li>
    <li><strong>Customizable Search Results</strong>: Specify the number of search results to retrieve.</li>
    <li><strong>Output Saving</strong>: Save findings to an output file.</li>
    <li><strong>Signal Handling</strong>: Gracefully handle interruptions and display collected results.</li>
</ul>

<h2>Installation</h2>
<p>Ensure you have Python 3 and the necessary dependencies installed:</p>
<pre><code>pip install requests beautifulsoup4 googlesearch-python colorama</code></pre>

<h2>Usage</h2>
<p>Run the tool from the command line using the following syntax:</p>
<pre><code>python3 test.py [options] [search_term]</code></pre>

<h3>Options</h3>
<ul>
    <li><code>-d</code>, <code>--dork</code>: Perform a dork scan using predefined queries.</li>
    <li><code>-n</code>, <code>--normal</code>: Perform a normal scan based on the search term.</li>
    <li><code>-a</code>, <code>--all</code>: Perform both dork and normal scans.</li>
    <li><code>-o</code>, <code>--output [filename]</code>: Save the results to the specified file.</li>
    <li><code>-u</code>, <code>--unavailable</code>: Show URLs that are unavailable.</li>
    <li><code>-v</code>, <code>--available</code>: Show URLs that are available.</li>
    <li><code>-s</code>, <code>--social</code>: Filter results to include only social media links.</li>
    <li><code>-f</code>, <code>--file</code>: Filter results to include only file links.</li>
    <li><code>-r</code>, <code>--results [number]</code>: Specify the number of search results to retrieve (default is 10).</li>
</ul>

<h3>Example</h3>
<p>1. <strong>Perform a dork scan with a specified number of results:</strong></p>
<pre><code>python3 test.py -d -r 20 "piyusha akash"</code></pre>

<p>2. <strong>Perform a normal scan and save results to a file:</strong></p>
<pre><code>python3 test.py -n -o results.txt "piyusha akash"</code></pre>

<p>3. <strong>Perform both dork and normal scans with filtering for social media links:</strong></p>
<pre><code>python3 test.py -a -s "piyusha akash"</code></pre>

<h2>Handling Interruptions</h2>
<p>To gracefully handle interruptions (e.g., Ctrl+C), the tool will display collected results and exit.</p>

<h2>Notes</h2>
<p class="note">Ensure you have an active internet connection to perform searches. The number of search results and specific filters can affect the performance and output of the tool.</p>

<h2>License</h2>
<p>This tool is provided as-is. Use it at your own risk.</p>

<h2>Contact</h2>
<p>For any issues or questions, please contact the maintainer at <a href="iakashwickramage@gmail.com">iakashwickramage@gmail.com</a>.</p>

</body>
</html>
