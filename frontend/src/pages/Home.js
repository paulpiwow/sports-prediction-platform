import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Sports Match Predictor</h1>

      <div className="card-grid">
        {/* Soccer Card */}
        <div
          className="sport-card"
          style={{
            backgroundImage: `
              linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)),
              url(${process.env.PUBLIC_URL}/soccer-bg.jpg)
            `,
            backgroundSize: "cover",
            backgroundPosition: "center"
          }}
          onClick={() => navigate("/soccer")}
        >
          <h2>⚽ World Cup Predictor</h2>
          <p>International match predictions</p>
        </div>

        {/* NBA Card */}
        <div
          className="sport-card"
          style={{
            backgroundImage: `
              linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)),
              url(${process.env.PUBLIC_URL}/nba-bg.jpg)
            `,
            backgroundSize: "cover",
            backgroundPosition: "center"
          }}
          onClick={() => navigate("/nba")}
        >
          <h2>🏀 NBA Predictor</h2>
          <p>NBA game predictions</p>
        </div>

        {/* NFL Card */}
        <div
          className="sport-card"
          style={{
            backgroundImage: `
      linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)),
      url(${process.env.PUBLIC_URL}/nfl-bg.jpg)
    `,
            backgroundSize: "cover",
            backgroundPosition: "center"
          }}
          onClick={() => navigate("/nfl")}
        >
          <h2>🏈 NFL Predictor</h2>
          <p>NFL game predictions</p>
        </div>

      </div>
    </div>
  );
}

