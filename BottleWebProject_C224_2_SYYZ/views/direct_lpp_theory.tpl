% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
	<h1>Direct linear programming problem</h1>
	<p class="lead">
       The direct linear programming problem task is to maximize or minimize the linear function of a goal under conditions expressed by a system of linear constraints.
    </p>
</div>

<div class="section">
    <h2>Problem Definition</h2>
    <p class="text">
        A primal linear programming problem (LPP) is an optimization task where you need to maximize or minimize a linear objective function
        <span class="center">Z = c<sub>1</sub>x<sub>1</sub> + c<sub>2</sub>x<sub>2</sub> + … + c<sub>n</sub>x<sub>n</sub></span>
        subject to a system of linear constraints, for example, a<sub>1</sub>x<sub>3</sub> + a<sub>2</sub>x<sub>5</sub> ≤ b<sub>1</sub> and non-negativity conditions xi ≥ 0.
    </p>
    <p class="text">The goal is to find such x<sub>i</sub> that Z is optimal.</p>
    <p class="text">The main method for solving a primal LPP is the simplex method.</p>
</div>

<section class="section">
    <h2>Simplex Method</h2>
    <p class="text">
        The Simplex Method is an algorithm for solving LPP, which works as follows:
    </p>
    <ol class="list">
        <li class="text">&emsp;Convert the problem to standard form by adding slack variables for inequalities.</li>
        <li class="text">&emsp;Construct the initial simplex table, where the rows are constraints, and the last row is the objective function.</li>
        <li class="text">&emsp;Iteratively:<br>
            <span class="step-item"><span>Check for optimality (are there negative coefficients in the Z-row?).</span></span>
            <span class="step-item"><span>If there are, select the pivot column (the largest negative number by modulus from the Z-row) and row (the minimum positive ratio of the right-hand side to the pivot column element), then update the table by introducing a new variable into the basis.</span></span>
            <span class="step-item"><span>Repeat until Z becomes optimal.</span></span>
            <span class="indented-text">All elements of the pivot row are divided by the pivot element, the elements of the pivot column are set to 0.</span>
            <span class="indented-text">The remaining elements are calculated using the formula:</span>
            <span class="formula">a<sub>ij</sub>' = a<sub>ij</sub> - (a<sub>iq</sub> * a<sub>pj</sub>) / a<sub>pq</sub>,</span>
            <span class="formula">where p is the pivot row, q is the pivot column</span>
        </li>
        <li class="text">&emsp;Extract the solution: the values of x<sub>i</sub> and Z.</li>
    </ol>
</section>

<p class="title-text">
	Example of Solving
</p>
<p class="intro-text">
	Maximize:
</p>
<p class="intro-text" style='text-align: center'>
Z = 3x<sub>1</sub> + 2x<sub>2</sub>
</p>
<p class="intro-text">
	Subject to:
</p>
<p class="intro-text" style='text-align: center'>
	2x<sub>1</sub> + x<sub>2</sub> ≤ 4 
</p>
<p class="intro-text" style='text-align: center'>
	x<sub>1</sub> + 2x<sub>2</sub> ≤ 4  
</p>
<p class="intro-text" style='text-align: center'>
	x<sub>1</sub>, x<sub>2</sub> ≥ 0
</p>
<p class="intro-text">
	Step 1: Convert to standard form
</p>
<p class="intro-text" style='text-align: center'>
	2x<sub>1</sub> + x<sub>2</sub> + s<sub>1</sub> = 4 
</p>
<p class="intro-text" style='text-align: center'>
	x<sub>1</sub> + 2x<sub>2</sub> + s<sub>2</sub> = 4 
</p>
<p class="intro-text" style='text-align: center'>
	Z = 3x<sub>1</sub> + 2x<sub>2</sub>,
</p>
<p class="intro-text">
	where s<sub>1</sub>, s<sub>2</sub> ≥ 0
</p>