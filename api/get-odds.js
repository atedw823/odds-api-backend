export default async function handler(req, res) {
  const { sport, market } = req.query;

  const url = `https://odds-api-backend.onrender.com/api/odds?sport=${sport}&market=${market}`;
  try {
    const response = await fetch(url);
    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch odds' });
  }
}
