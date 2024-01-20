

% Original data
theta = pi/6 ; 

P  = cos(theta/2)^2 

d_l = 0.03 ; % error between the estimate proportion pl and the true proportion P
e_l = 0.05 ; % e_l as the probability of such an error (e_l can be understood as the risk we are willing to take).

%% What mean and var should this have ? 
tl = norminv(e_l) ; % where tl is the value of the abscissa axis for which e_l of the area under the normal curve lies to the right of tl.

Ml =  ceil( tl ^ 2 / ( 4 * d_l ^ 2) ) ; 


r = 1 ;     % subsets Ml
M = r*Ml ;   % Number of measurements

q = rand(Ml , r ) < P ;


p_l = sum(q) / Ml ; % pl = m1l / (m1l + m2l)
G  = 2*acos(sqrt(p_l)) ; 

%% Other way
alpha = 0.05 ; 
% Clopper-Pearson method
[phat,pci] = binofit(sum(q,'all'),M,alpha) 

% Normal approximation interval or Wald interval
Z = norminv(alpha/2) ;
p_hat = mean(p_l);
ci =  -(Z * sqrt(p_hat*(1-p_hat)/M)) * [-1 1] + p_hat 




%% Algorithm 3 
m_theta = mean(G) ; 
var_theta = var(G) ; 
S = std(G) ; 

var_hat = 2 * S^2 / r ;


%% Plots
figure; 
histfit(G);
title("θ histogram")
ylabel("Absolute frequency")

figure; 
histfit(p_l)
title("p_l histogram")
ylabel("Absolute frequency")


x = (m_theta - theta)-3*sqrt(var_hat):3*sqrt(var_hat)/10000:(m_theta - theta)+3*sqrt(var_hat);
y = normpdf(x ,m_theta - theta ,    sqrt(var_hat)); 
figure; 
plot(x,y)
title("g distribution (for the mean of the set G)")
ylabel('Probability Density')





