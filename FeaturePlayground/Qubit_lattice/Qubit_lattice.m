% Quantum Image Encoding in Qubit Lattice
% This script illustrates the encoding of information, represented by the
% angle theta, into a quantum state within a Qubit Lattice. The example
% focuses on a single pixel, demonstrating the encoding process across
% multiple qubits. Subsequently, the script performs the estimation
% (reading) of the encoded information.


% Original data
theta = pi/3 ; % Angle in range [0, pi]

d_l = 0.05 ; % Error between the estimated proportion p_l and the true proportion P
alpha = 0.05 ; % alpha / e_l is the probability of such an error

% |ψ> = cos( θ/2 ) |0> + e^(iγ) sin( θ/2 ) |1>

% Probability of the qubit mesurement being 1
P  = cos(theta/2)^2 ;
f = @(x) 2*acos(sqrt(x)) ; % Inverse to calculate theta from p 


% Calculate the value of the abscissa axis for which e_l of the area under
% the normal curve lies to the right of tl
tl = norminv(alpha) ; 

% Determine the number of measurements required for desired estimation
Ml =  ceil( tl ^ 2 / ( 4 * d_l ^ 2) ) ; 


r = 1  ;        % subsets Ml
M = r*Ml ;      % Number of measurements

% "Create and Measure" the qubits
q = rand(Ml , r ) < P ;


% Calculate the estimate of the proportion p_l
p_l = sum(q) / Ml ; % pl = m1l / (m1l + m2l)

% Calculate the angle G using the estimates
G  = f(p_l) ; 



%% Estimation
% Clopper-Pearson method to estimate Binomial parameters (p and a ci)
[phat_CP,pci_CP] = binofit(sum(q,'all'),M,alpha) ;

% Normal approximation interval or Wald interval
Z = norminv(alpha/2) ;
phat_Wald = mean(p_l);
ci_Wald =  -(Z * sqrt(phat_Wald*(1-phat_Wald)/M)) * [-1 1] + phat_Wald ;


%% Display the results 
fprintf("Total measurments %d \n\n", M ); 

% Display the original probability P and the estimate G
fprintf('Original Angle (theta): %.4f [rad]\n', theta);
fprintf('Original Probability (P): %.4f\n\n', P);

fprintf('Clopper-Pearson Method:\n');
fprintf('Estimated Angle (theta): %.4f\n', f(phat_CP) );
fprintf('Confidence Interval Angle (theta): [%.4f, %.4f]\n', f(pci_CP));
fprintf('Estimated Probability (phat): %.4f\n', phat_CP);
fprintf('Confidence Interval (Clopper-Pearson): [%.4f, %.4f]\n\n', pci_CP);

fprintf('Normal Approximation Interval (Wald Interval):\n');
fprintf('Estimated Angle (theta): %.4f\n', f(phat_Wald) );
fprintf('Confidence Interval Angle (theta): [%.4f, %.4f]\n', f(ci_Wald));
fprintf('Estimated Probability (p_hat): %.4f\n', phat_Wald);
fprintf('Confidence Interval (Wald Interval): [%.4f, %.4f]\n', ci_Wald);

fprintf("Total measurments %d \n\n", M ); 

names = ["Original" "Estimate" "CI_Clopper-Pearson" "CI_Wald"] ; 
originalDataTable = table(names' , [P phat_CP {pci_CP} {ci_Wald}]' , [theta f(phat_CP)  {f(pci_CP)} {f(ci_Wald)}]', ...
    'VariableNames', {'categories', 'p' , 'theta [rad]'});

disp(originalDataTable)

%% Plots
if r > 1 
    figure; 
    histfit(G);
    title("θ histogram")
    ylabel("Absolute frequency")
    xline(theta,'r','Original','DisplayName','Original theta','LabelHorizontalAlignment','center')
    xline(f(phat_CP),'r','Estimate','DisplayName','Estimate theta','LabelHorizontalAlignment','center')
    
    figure; 
    histfit(p_l)
    title("p_l histogram")
    ylabel("Absolute frequency")
    xline(P,'r','Original','DisplayName','Original p','LabelHorizontalAlignment','center')
    xline(phat_CP,'r','Estimate','DisplayName','Estimate p','LabelHorizontalAlignment','center')
end


% %% Algorithm 3 
% m_theta = mean(G) ; 
% var_theta = var(G) ; 
% S = std(G) ; 
% 
% var_hat = 2 * S^2 / r ;



% figure;
% x = (m_theta - theta)-3*sqrt(var_hat):3*sqrt(var_hat)/10000:(m_theta - theta)+3*sqrt(var_hat);
% y = normpdf(x ,m_theta - theta ,    sqrt(var_hat));  
% plot(x,y)
% title("g distribution (for the mean of the set G)")
% ylabel('Probability Density')





